---
title: README
author: Jan-Michael Rye
---

# Synopsis

A context manager for rudimentary file locking. Lock files are generated next to the target path using the current hostname, process ID (PID) and a random hexadecimal token. Access to the file is then granted in order of ascending modification times of the associated lock files. If two or more lock files for the same path have the same modification time, access is granted in the sort order of the lock file paths. Each context waits for its turn to access the file.

The associated lock file is deleted on exit from the context. The context also automatically deletes dead lock files for non-existent processes on the same host. Dead locks are detected by checking if the associated process has exited with [psutil](https://pypi.org/project/psutil/).

# Links

* [Homepage](https://gitlab.inria.fr/jrye/simple-file-lock)
* [Repository](https://gitlab.inria.fr/jrye/simple-file-lock.git)
* [Documentation](https://jrye.gitlabpages.inria.fr/simple-file-lock)
* [Issues](https://gitlab.inria.fr/jrye/simple-file-lock/-/issues)
* [PyPI Package](https://pypi.org/project/simple-file-lock/)
* [Software Heritage](https://archive.softwareheritage.org/browse/origin/?origin_url=https%3A//gitlab.inria.fr/jrye/simple-file-lock.git)

# Usage

~~~python
from simple_file_lock import FileLock

# ...

# Gain exclusive access to a path by creating a context with FileLock:
with FileLock(path):
  # Do whatever you want with the file here. When the context is exited, the
  # lock is released.
~~~

`FileLock` also accepts an `interval` parameter to configure the polling interval when waiting for existing locks to be released.

The Sphinx-generated API documentation is available [here](https://jrye.gitlabpages.inria.fr/simple-file-lock/).

# Unit Tests

Some basic unit tests have been implemented and can be run in a virtual environment with [test.sh](scripts/test.sh).
