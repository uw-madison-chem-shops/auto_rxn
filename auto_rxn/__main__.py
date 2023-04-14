#!/usr/bin/env python3

import click

from ._happi import happi_client
from .__version__ import __version__


@click.group()
@click.version_option(__version__)
def main():
    pass

@main.command(name="list_devices")
def _list_devices():
    for item, result in happi_client.items():
        print(item)
        print(f"    device_class: {result.metadata['device_class']}")

@main.command(name="run")
def _run():
    print("run not yet implemented, exiting")
