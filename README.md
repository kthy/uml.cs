# uml.cs

UML class diagram generator for C# code.

[![Python 3](https://pyup.io/repos/github/kthy/uml.cs/python-3-shield.svg)](https://pyup.io/repos/github/kthy/uml.cs/)
[![Build Status](https://travis-ci.org/kthy/uml.cs.svg?branch=master)](https://travis-ci.org/kthy/uml.cs)
[![Codecov Status](https://codecov.io/gh/kthy/uml.cs/branch/master/graph/badge.svg)](https://codecov.io/gh/kthy/uml.cs)
[![Requirements Status](https://requires.io/github/kthy/uml.cs/requirements.svg?branch=master)](https://requires.io/github/kthy/uml.cs/requirements/?branch=master)
[![Updates](https://pyup.io/repos/github/kthy/uml.cs/shield.svg)](https://pyup.io/repos/github/kthy/uml.cs/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

## Development environment setup

Ubuntu on WSL:

```bash
$ sudo apt install graphviz
…
The following NEW packages will be installed:
  fonts-liberation graphviz libann0 libcdt5 libcgraph6 libgd3 libgts-0.7-5 libgts-bin libgvc6 libgvpr2 liblab-gamut1 libpathplan4
0 upgraded, 12 newly installed, 0 to remove and 0 not upgraded.
…
$ which python
/usr/bin/python
$ `which python` -V
Python 2.7.17
$ `which python3` -V
Python 3.6.9
$ sudo apt install python3-pip
…
0 upgraded, 14 newly installed, 0 to remove and 0 not upgraded.
…
$ pip3 --version
pip 9.0.1 from /usr/lib/python3/dist-packages (python 3.6)
$ pip3 install --user pipenv
Successfully installed certifi-2019.11.28 pip-20.0.2 pipenv-2018.11.26 setuptools-45.1.0 virtualenv-16.7.9 virtualenv-clone-0.5.3
$ pipenv --version
pipenv: command not found
$ python -m site --user-base
/home/thy/.local
$ `python -m site --user-base`/bin/pipenv --version
pipenv, version 2018.11.26
$ . .profile
$ pipenv --version
pipenv, version 2018.11.26
```

(This was the first install in `~/.local/bin/`, hence it wasn't on the `PATH`.)
