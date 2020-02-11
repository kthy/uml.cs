# -*- coding: utf-8 -*-
"""CLI entrypoint."""

from glob import glob
from os.path import join
from re import search
from subprocess import run  # nosec

import click

try:
    from creator import UmlCreator
except (ImportError, ModuleNotFoundError):  # pragma: no cover
    from umldotcs.creator import UmlCreator

NAMESPACES = dict()
RELATIONS = []

# TODO: add option for exclusions
@click.command()
@click.argument("directory")
@click.option("-f", "--font", default="Bahnschrift")
@click.option("-l", "--label", default="UML Diagram")
@click.option("-o", "--output-gv", required=True)
@click.option("-s", "--output-svg")
@click.option("-u", "--repo-url")
def create_uml(directory, font, label, output_gv, output_svg, repo_url):
    """Process all .cs files in directory and its sub-directories."""
    files = [f for f in glob(join(directory, "**", "*.cs"), recursive=True) if not exclude(f)]
    print(f"Processing {files}")
    for file_path in files:
        uml_creator = UmlCreator(file_path, repo_url)
        nsp, rel = uml_creator.process_file()
        zip_namespaces(nsp)
        RELATIONS.extend(rel)
    if NAMESPACES:
        UmlCreator.write_gv(output_gv, label, font, NAMESPACES, RELATIONS)
        if output_svg:
            run(["dot", "-Tsvg", "-o", output_svg, output_gv], check=False)
    else:
        print("NO CODE")


def exclude(path):
    """Return True if the path should be excluded."""
    return search(r"AssemblyInfo\.cs|Test\.cs|/(bin|obj)/(Debug|Release)/", path)


def zip_namespaces(nsp):
    """Merge namespace dictionaries."""
    for key, val in nsp.items():
        if key in NAMESPACES:
            NAMESPACES[key].extend(val)
        else:
            NAMESPACES[key] = val
