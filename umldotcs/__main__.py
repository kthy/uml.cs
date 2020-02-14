#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Main entrypoint for the uml.cs CLI."""

from umldotcs.cli import create_uml

if __name__ == "__main__":
    # Click magically transforms the call, but pylint doesn't grok it…
    # pylint: disable=no-value-for-parameter,unexpected-keyword-arg
    create_uml(prog_name="umldotcs")
