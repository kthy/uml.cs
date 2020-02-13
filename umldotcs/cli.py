# -*- coding: utf-8 -*-
"""CLI entrypoint."""

from glob import glob
from os.path import join
from re import search
from subprocess import CalledProcessError, run  # nosec

import click

from umldotcs.creator import UmlCreator

NAMESPACES = dict()
RELATIONS = list()

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
    files = glob_files(directory)
    for file_path in files:
        click.echo(f"Processing {click.format_filename(file_path)[len(directory):]}")
        nsp, rel = UmlCreator(file_path, repo_url).process_file()
        zip_namespaces(nsp)
        zip_relations(rel)
    write_output(font, label, output_gv, output_svg)


def glob_files(directory):
    """Return list of non-excluded files in dir and its subdirs."""
    return [f for f in glob(join(directory, "**", "*.cs"), recursive=True) if not exclude(f)]


def exclude(path):
    """Return True if the path should be excluded."""
    return search(r"AssemblyInfo\.cs|Test\.cs|/(bin|obj)/(Debug|Release)/", path)


def write_output(font, label, output_gv, output_svg):
    """Write GraphViz file and optionally run dot to convert it to SVG."""
    if NAMESPACES:
        UmlCreator.write_gv(output_gv, label, font, NAMESPACES, RELATIONS)
        if output_svg:
            try:
                run(["dot", "-Tsvg", "-o", output_svg, output_gv], check=True)
            except CalledProcessError:
                return 2
    else:
        click.secho("NO CODE", fg="bright_red", bold=True)
    return 0


def zip_namespaces(nsp):
    """Merge namespace dictionaries."""
    for key, val in nsp.items():
        if key in NAMESPACES:
            NAMESPACES[key].extend(val)
        else:
            NAMESPACES[key] = val


def zip_relations(rel):
    """Append relations to global list."""
    RELATIONS.extend(rel)
