"""
some io utils to handle `nexus <https://manual.nexusformat.org/index.html>`_ and `hdf5 <https://www.hdfgroup.org/solutions/hdf5/>`_ with `h5py <https://www.h5py.org/>`_
"""
import errno
import logging
import os
import traceback
from contextlib import ExitStack, contextmanager
import h5py._hl.selections as selection
from silx.io.url import DataUrl

import h5py
import threading


HASSWMR = h5py.version.hdf5_version_tuple >= h5py.get_config().swmr_min_hdf5_version
_logger = logging.getLogger(__name__)


class SharedLockPool:
    """
    Allows to acquire locks identified by name (hashable type) recursively.
    """

    def __init__(self):
        self.__locks = {}
        self.__locks_mutex = threading.Semaphore(value=1)

    def __len__(self):
        return len(self.__locks)

    @property
    def names(self):
        return list(self.__locks.keys())

    @contextmanager
    def _modify_locks(self):
        self.__locks_mutex.acquire()
        try:
            yield self.__locks
        finally:
            self.__locks_mutex.release()

    @contextmanager
    def acquire(self, name):
        with self._modify_locks() as locks:
            lock = locks.get(name, None)
            if lock is None:
                locks[name] = lock = threading.RLock()
        lock.acquire()
        try:
            yield
        finally:
            lock.release()
            with self._modify_locks() as locks:
                if name in locks:
                    locks.pop(name)

    @contextmanager
    def acquire_context_creation(self, name, contextmngr, *args, **kwargs):
        """
        Acquire lock only during context creation.

        This can be used for example to protect the opening of a file
        but not hold the lock while the file is open.
        """
        with ExitStack() as stack:
            with self.acquire(name):
                ret = stack.enter_context(contextmngr(*args, **kwargs))
            yield ret


class HDF5File(h5py.File):
    """
    File to secure reading and writing within h5py

    code originally from bliss.nexus_writer_service.io.nexus
    """

    _LOCKPOOL = SharedLockPool()

    def __init__(self, filename, mode, enable_file_locking=None, swmr=None, **kwargs):
        """
        :param str filename:
        :param str mode:
        :param bool enable_file_locking: by default it is disabled for `mode=='r'`
                                         and enabled in all other modes
        :param bool swmr: when not specified: try both modes when `mode=='r'`
        :param **kwargs: see `h5py.File.__init__`
        """
        if mode not in ("r", "w", "w-", "x", "a"):
            raise ValueError(f"invalid mode {mode}")

        with self._protect_init(filename):
            # https://support.hdfgroup.org/HDF5/docNewFeatures/SWMR/Design-HDF5-FileLocking.pdf
            if not HASSWMR and swmr:
                swmr = False
            libver = kwargs.get("libver")
            if swmr:
                kwargs["libver"] = "latest"
            if enable_file_locking is None:
                enable_file_locking = mode != "r"
            old_file_locking = os.environ.get("HDF5_USE_FILE_LOCKING", None)
            if enable_file_locking:
                os.environ["HDF5_USE_FILE_LOCKING"] = "TRUE"
            else:
                os.environ["HDF5_USE_FILE_LOCKING"] = "FALSE"
            kwargs["track_order"] = True
            try:
                super().__init__(filename, mode=mode, swmr=swmr, **kwargs)
                if mode != "r" and swmr:
                    # Try setting writing in SWMR mode
                    try:
                        self.swmr_mode = True
                    except Exception:
                        pass
            except OSError as e:
                if (
                    swmr is not None
                    or mode != "r"
                    or not HASSWMR
                    or not isErrno(e, errno.EAGAIN)
                ):
                    raise
                # Try reading with opposite SWMR mode
                swmr = not swmr
                if swmr:
                    kwargs["libver"] = "latest"
                else:
                    kwargs["libver"] = libver
                super().__init__(filename, mode=mode, swmr=swmr, **kwargs)
            if old_file_locking is None:
                del os.environ["HDF5_USE_FILE_LOCKING"]
            else:
                os.environ["HDF5_USE_FILE_LOCKING"] = old_file_locking

    @contextmanager
    def _protect_init(self, filename):
        """Makes sure no other file is opened/created
        or protected sections associated to the filename
        are executed.
        """
        lockname = os.path.abspath(filename)
        with self._LOCKPOOL.acquire(None):
            with self._LOCKPOOL.acquire(lockname):
                yield

    @contextmanager
    def protect(self):
        """Protected section associated to this file."""
        lockname = os.path.abspath(self.filename)
        with self._LOCKPOOL.acquire(lockname):
            yield


def isErrno(e, errno):
    """
    check if the errno happen

    :param OSError e:
    :returns bool:
    """
    # Because e.__cause__ is None for chained exceptions
    return f"errno = {errno}" in "".join(traceback.format_exc())


def check_virtual_sources_exist(fname, data_path):
    """
    Check that a virtual dataset points to actual data.

    :param str fname: HDF5 file path
    :param str data_path: Path within the HDF5 file

    :return bool res: Whether the virtual dataset points to actual data.
    """
    with HDF5File(fname, "r") as f:
        if data_path not in f:
            _logger.error(f"No dataset {data_path} in file {fname}")
            return False
        dptr = f[data_path]
        if not dptr.is_virtual:
            return True
        for vsource in dptr.virtual_sources():
            vsource_fname = os.path.join(
                os.path.dirname(dptr.file.filename), vsource.file_name
            )
            if not os.path.isfile(vsource_fname):
                _logger.error(f"No such file: {vsource_fname}")
                return False
            elif not check_virtual_sources_exist(vsource_fname, vsource.dset_name):
                _logger.error(f"Error with virtual source {vsource_fname}")
                return False
    return True


def from_data_url_to_virtual_source(url: DataUrl) -> tuple:
    """
    convert a DataUrl to a set (as tuple) of h5py.VirtualSource

    :param DataUrl url: url to be converted to a virtual source. It must target a 2D detector
    :return: (h5py.VirtualSource, tuple(shape of the virtual source), numpy.drype: type of the dataset associated with the virtual source)
    :rtype: tuple
    """
    if not isinstance(url, DataUrl):
        raise TypeError(
            f"url is expected to be an instance of DataUrl and not {type(url)}"
        )

    with HDF5File(url.file_path(), mode="r") as o_h5s:
        original_data_shape = o_h5s[url.data_path()].shape
        data_type = o_h5s[url.data_path()].dtype
        if len(original_data_shape) == 2:
            original_data_shape = (
                1,
                original_data_shape[0],
                original_data_shape[1],
            )

        vs_shape = original_data_shape
        if url.data_slice() is not None:
            vs_shape = (
                url.data_slice().stop - url.data_slice().start,
                original_data_shape[-2],
                original_data_shape[-1],
            )

    vs = h5py.VirtualSource(
        url.file_path(), url.data_path(), shape=vs_shape, dtype=data_type
    )

    if url.data_slice() is not None:
        vs.sel = selection.select(original_data_shape, url.data_slice())
    return vs, vs_shape, data_type


def from_virtual_source_to_data_url(vs: h5py.VirtualSource) -> DataUrl:
    """
    convert a h5py.VirtualSource to a DataUrl

    :param h5py.VirtualSource vs: virtual source to be converted to a DataUrl
    :return: url
    :rtype: DataUrl
    """
    if not isinstance(vs, h5py.VirtualSource):
        raise TypeError(
            f"vs is expected to be an instance of h5py.VirtualSorce and not {type(vs)}"
        )
    url = DataUrl(file_path=vs.path, data_path=vs.name, scheme="silx")
    return url


@contextmanager
def cwd_context(new_cwd=None):
    """
    create a context with 'new_cwd'.

    on entry update current working directory to 'new_cwd' and reset previous 'working_directory' at exit
    :param Optional[str] new_cwd: current working directory to use in the context
    """
    try:
        curdir = os.getcwd()
    except Exception as e:
        _logger.error(e)
        curdir = None
    try:
        if new_cwd is not None and os.path.isfile(new_cwd):
            new_cwd = os.path.dirname(new_cwd)
        if new_cwd not in (None, ""):
            os.chdir(new_cwd)
        yield
    finally:
        if curdir is not None:
            os.chdir(curdir)


def to_target_rel_path(file_path: str, target_path: str) -> str:
    """
    cast file_path to a relative path according to target_path.
    This is used to deduce h5py.VirtualSource path

    :param str file_path: file path to be moved to relative
    :param str target_path: target used as 'reference' to get relative path
    :return: relative path of file_path compared to target_path
    :rtype: str
    """
    file_path = os.path.realpath(file_path)
    target_path = os.path.realpath(target_path)
    path = os.path.relpath(file_path, os.path.dirname(target_path))
    if not path.startswith("./"):
        path = "./" + path
    return path
