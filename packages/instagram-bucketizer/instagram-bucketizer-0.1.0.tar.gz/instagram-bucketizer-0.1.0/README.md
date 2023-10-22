<!--
    =====================================
    generator=datazen
    version=3.1.4
    hash=433bf8944d18413ea24ab46e37345bd2
    =====================================
-->

# instagram-bucketizer ([0.1.0](https://pypi.org/project/instagram-bucketizer/))

[![python](https://img.shields.io/pypi/pyversions/instagram-bucketizer.svg)](https://pypi.org/project/instagram-bucketizer/)
![Build Status](https://github.com/dylanfromm/instagram-bucketizer/workflows/Python%20Package/badge.svg)
[![codecov](https://codecov.io/gh/dylanfromm/instagram-bucketizer/branch/master/graphs/badge.svg?branch=master)](https://codecov.io/github/dylanfromm/instagram-bucketizer)
![PyPI - Status](https://img.shields.io/pypi/status/instagram-bucketizer)
![Dependents (via libraries.io)](https://img.shields.io/librariesio/dependents/pypi/instagram-bucketizer)

*Small project to assist in research, categorizing instagram emoji usage*

## Documentation

### Generated

* By [sphinx-apidoc](https://dylanfromm.github.io/python/sphinx/instagram-bucketizer)
(What's [`sphinx-apidoc`](https://www.sphinx-doc.org/en/master/man/sphinx-apidoc.html)?)
* By [pydoc](https://dylanfromm.github.io/python/pydoc/instagram_bucketizer.html)
(What's [`pydoc`](https://docs.python.org/3/library/pydoc.html)?)

## Python Version Support

This package is tested with the following Python minor versions:

* [`python3.8`](https://docs.python.org/3.8/)
* [`python3.9`](https://docs.python.org/3.9/)
* [`python3.10`](https://docs.python.org/3.10/)
* [`python3.11`](https://docs.python.org/3.11/)

## Platform Support

This package is tested on the following platforms:

* `ubuntu-latest`
* `macos-latest`
* `windows-latest`

# Introduction

# Command-line Options

```
$ ./venv3.11/bin/instagram-bucketizer -h

usage: instagram-bucketizer [-h] [--version] [-v] [-q] [--curses]
                            [--no-uvloop] [-C DIR]
                            {bucketize,parse_post,setup_session,noop} ...

Small project to assist in research, categorizing instagram emoji usage

options:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -v, --verbose         set to increase logging verbosity
  -q, --quiet           set to reduce output
  --curses              whether or not to use curses.wrapper when starting
  --no-uvloop           whether or not to disable uvloop as event loop driver
  -C DIR, --dir DIR     execute from a specific directory

commands:
  {bucketize,parse_post,setup_session,noop}
                        set of available commands
    bucketize           bucketize comments
    parse_post          parse a given post short code
    setup_session       Used firefox cookies to setup session file
    noop                command stub (does nothing)

```

# Internal Dependency Graph

A coarse view of the internal structure and scale of
`instagram-bucketizer`'s source.
Generated using [pydeps](https://github.com/thebjorn/pydeps) (via
`mk python-deps`).

![instagram-bucketizer's Dependency Graph](im/pydeps.svg)
