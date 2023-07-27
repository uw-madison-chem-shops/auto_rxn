#!/usr/bin/env python3

import click

from ._device import happi_client
from .__version__ import __version__
from ._recipe import Recipe
from ._run import run


@click.group()
@click.version_option(__version__)
def main():
    pass


@main.command(name="list_devices")
def _list_devices():
    for item, result in happi_client.items():
        print(item)
        print(f"    device_class: {result.metadata['device_class']}")
        try:
            print(f"    lower_safety_limit: {result.metadata['auto_rxn_lower_safety_limit']}")
        except KeyError:
            print(f"    lower_safety_limit: None")
        try:
            print(f"    upper_safety_limit: {result.metadata['auto_rxn_upper_safety_limit']}")
        except KeyError:
            print(f"    upper_safety_limit: None")
        try:
            print(f"    fallback_posiiton: {result.metadata['auto_rxn_fallback_position']}")
        except KeyError:
            print(f"    fallback_posiiton: None")


@main.command(name="run")
@click.argument("recipe", type=click.Path())
def _run(recipe):
    r = Recipe(recipe)
    run(r)
