#!/usr/bin/env python3

'''
Rudimentary interprocess file locking.
'''

import contextlib
import logging
import os
import pathlib
import platform
import secrets
import time

import psutil


LOGGER = logging.getLogger(__name__)


class FileLock():
    '''
    Context manager for acquiring exclusive access to files via file locks

    Lock files are created adjacent to the target file using a naming scheme
    that included the running process' hostname and process ID (PID). The
    directory is then scanned for other lock files for the same target file. If
    any are found, the lock files are ordered by ascending modification time and
    by ascending PID for files with the same modification time. The context
    manager will continue to scan the directory and wait until all previous lock
    files are removed before proceeding.

    Leftover lock files from processes that are no longer running on the same
    machine will be automatically removed.
    '''
    def __init__(self, path, interval=0.1):
        '''
        Args:
            path:
                The filepath to lock.

            interval:
                The interval to wait between subsequent checks.
        '''
        self.path = pathlib.Path(path).resolve()
        self.my_pid = os.getpid()
        self.my_hostname = platform.node().replace(os.sep, '_')
        self.my_pid_path = None
        self.interval = float(interval)

    def create_lock(self):
        '''
        Attempt to create a unique lock. This will check for existing locks from
        the same process and attempt to handle races within the same process.

        Returns:
            The lock file path.
        '''
        parent_dir = self.path.parent
        encoding = 'utf-8'
        while True:
            path = parent_dir / (
                f'{self.path.name}.lock'
                f'.{self.my_hostname}.{self.my_pid}.{secrets.token_hex(32)}.pid'
            )
            if not path.exists():
                LOGGER.debug('Creating lock file: %s', path)
                path.write_text(f'{self.my_pid}', encoding=encoding)
                return path
        return None

    def __enter__(self):
        parent_dir = self.path.parent

        # Create the parent directory because the target path may not yet exist.
        parent_dir.mkdir(parents=True, exist_ok=True)

        self.my_pid_path = self.create_lock()
        my_mtime = self.my_pid_path.stat().st_mtime

        LOGGER.debug('Attempting to acquire access to %s', self.path)
        while True:
            first = True
            for pid_path in parent_dir.glob(f'{self.path.name}.lock.*.pid'):
                if pid_path == self.my_pid_path:
                    continue

                hostname = pid_path.suffixes[-4][1:]
                pid = int(pid_path.suffixes[-3][1:])

                # Remove dead locks.
                if hostname == self.my_hostname and not psutil.pid_exists(pid):
                    LOGGER.warning('Removing dead lock file: %s', pid_path)
                    try:
                        pid_path.unlink()
                    except FileNotFoundError:
                        pass
                    continue

                try:
                    mtime = pid_path.stat().st_mtime
                except FileNotFoundError:
                    continue

                if mtime < my_mtime:
                    first = False
                    break

                if mtime == my_mtime:
                    if pid_path < self.my_pid_path:
                        first = False
                        break

            if first:
                LOGGER.debug('Acquired access to %s', self.path)
                return self.path

            time.sleep(self.interval)

    def __exit__(self, typ, val, traceback):
        if self.my_pid_path is not None:
            self.my_pid_path.unlink()


@contextlib.contextmanager
def MultiFileLock(paths, **kwargs):  # pylint: disable=invalid-name
    '''
    Context manager for locking multiple files with FileLock.

    Args:
        paths:
            An iterable of paths to lock.

        **kwargs:
            Keyword arguments passed through to FileLock.

    Returns:
        A list of locked paths.
    '''
    with contextlib.ExitStack() as stack:
        yield [stack.enter_context(FileLock(path, **kwargs)) for path in paths]
