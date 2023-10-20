from datetime import timedelta, datetime
from functools import lru_cache, wraps
from zlib import adler32
from pathlib import Path
import contextlib
import os


def text_file_checksum(path: Path):
    """
    Returns the adler32 hash of the contents of a text file. Adler32 was used because it was faster than md5, there are
    certainly faster alternative I don't know about.
    :param path: path to the text file
    :return:
    """
    encoding = 'utf-8'
    # Decoding/encoding is done to stay invariant to different line endings.
    return adler32(path.read_text(encoding=encoding).encode(encoding=encoding))


class OutputExistsError(Exception):
    """
    Raised when a function crates output files and some of them already exist.
    """
    def __init__(self, paths):
        """
        Paths
        :param paths: the paths to the output files that already exist.
        """
        self.paths = paths
        message = 'Some of the output files already exist'
        if paths:
            message += ':\n\n' + '\n'.join((str(path.absolute()) for path in paths))
        super().__init__(message)


# copied from
@contextlib.contextmanager
def modified_environ(*remove, **update):
    """
    Temporarily updates the ``os.environ`` dictionary in-place.
    The ``os.environ`` dictionary is updated in-place so that the modification
    is sure to work in all situations.
    :param remove: Environment variables to remove.
    :param update: Dictionary of environment variables and values to add/update.
    """
    env = os.environ
    update = update or {}
    remove = remove or []

    # List of environment variables being updated or removed.
    stomped = (set(update.keys()) | set(remove)) & set(env.keys())
    # Environment variables and values to restore on exit.
    update_after = {k: env[k] for k in stomped}
    # Environment variables and values to remove on exit.
    remove_after = frozenset(k for k in update if k not in env)

    try:
        env.update(update)
        [env.pop(k, None) for k in remove]
        yield
    finally:
        env.update(update_after)
        [env.pop(k) for k in remove_after]


def df_to_list_of_tuples(df):
    return list(df.to_records(index=False))


def timed_lru_cache(seconds: int, maxsize: int = None):
    """
    Cache the results of a function for a specified number of seconds. Upon expiration, clear the whole cache,
    not one value at a time.

    Copied verbatim from https://www.mybluelinux.com/pyhon-lru-cache-with-time-expiration/
    :param seconds: number of seconds the cache will persist, resets after cache expires.
    :param maxsize: as in lru_cache
    :return:
    """
    def wrapper_cache(func):
        print('I will use lru_cache')
        func = lru_cache(maxsize=maxsize)(func)
        print('I\'m setting func.lifetime')
        func.lifetime = timedelta(seconds=seconds)
        print('I\'m setting func.expiration')
        func.expiration = datetime.utcnow() + func.lifetime

        @wraps(func)
        def wrapped_func(*args, **kwargs):
            print('Check func expiration')
            print(f'datetime.utcnow(): {datetime.utcnow()}, func.expiration: {func.expiration}')
            if datetime.utcnow() >= func.expiration:
                print('func.expiration lru_cache lifetime expired')
                func.cache_clear()
                func.expiration = datetime.utcnow() + func.lifetime

            return func(*args, **kwargs)

        return wrapped_func

    return wrapper_cache
