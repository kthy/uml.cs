#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Main entrypoint for the uml.cs CLI."""                                         # pragma: no cover

try:                                                                              # pragma: no cover
    from cli import create_uml
except (ImportError, ModuleNotFoundError):                                        # pragma: no cover
    from umldotcs.cli import create_uml

if __name__ == "__main__":                                                        # pragma: no cover
    create_uml()                                            # pylint: disable=no-value-for-parameter
