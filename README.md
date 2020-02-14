![Uml.C#](https://repository-images.githubusercontent.com/238708889/14df4f80-4f3d-11ea-80c3-462fae3affa3)

# Uml.cs

UML class diagram generator for C# code.

### Code

[![Requirements Status](https://requires.io/github/kthy/uml.cs/requirements.svg?branch=master)](https://requires.io/github/kthy/uml.cs/requirements/?branch=master)
[![Updates](https://pyup.io/repos/github/kthy/uml.cs/shield.svg)](https://pyup.io/repos/github/kthy/uml.cs/)
[![Conventional commits](https://img.shields.io/badge/conventional%20commits-1.0.0-blue.svg)](https://www.conventionalcommits.org/en/v1.0.0/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

### CI

[![Build Status](https://travis-ci.org/kthy/uml.cs.svg?branch=master)](https://travis-ci.org/kthy/uml.cs)
[![Codecov Status](https://codecov.io/gh/kthy/uml.cs/branch/master/graph/badge.svg)](https://codecov.io/gh/kthy/uml.cs)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=kthy_uml.cs&metric=alert_status)](https://sonarcloud.io/dashboard?id=kthy_uml.cs)
[![Technical Debt](https://sonarcloud.io/api/project_badges/measure?project=kthy_uml.cs&metric=sqale_index)](https://sonarcloud.io/dashboard?id=kthy_uml.cs)

## Usage

```bash
$ python3 -m umldotcs --help
Usage: umldotcs [OPTIONS] DIRECTORY

  Process all .cs files in directory and its sub-directories.

Options:
  -f, --font TEXT
  -l, --label TEXT
  -o, --output-gv TEXT   [required]
  -s, --output-svg TEXT
  -u, --repo-url TEXT
  --help                 Show this message and exit.
```

## Development environment setup

Ubuntu on WSL:

```bash
$ sudo apt install graphviz
$ sudo apt install python3-pip
$ pip3 install --user pipenv
$ . .profile
$ pipenv --version
pipenv, version 2018.11.26
```
