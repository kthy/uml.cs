#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Main entrypoint for the uml.cs CLI."""

try:
    from cli import create_uml
except (ImportError, ModuleNotFoundError):
    from umldotcs.cli import create_uml

if __name__ == "__main__":
    create_uml()  # pylint: disable=no-value-for-parameter
