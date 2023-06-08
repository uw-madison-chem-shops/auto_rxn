# auto_rxn

[![PyPI](https://img.shields.io/pypi/v/auto_rxn)](https://pypi.org/project/auto_rxn)
[![Conda](https://img.shields.io/conda/vn/conda-forge/auto_rxn)](https://anaconda.org/conda-forge/auto_rxn)
[![log](https://img.shields.io/badge/change-log-informational)](https://github.com/uw-madison-chem-shops/auto_rxn/-/blob/main/CHANGELOG.md)

Python package for running chemical reactions as defined by "recipe" files.

Credit for original design of this interface goes to Unni Kurumbail of the Herman's Group at University of Wisconsin-Madison Chemistry Department.
https://github.com/ukurumbail/auto_rxn

## installation

TODO

## usage

`auto_rxn` is primarily a command-line Python application.
Once hardware is configured, reactions can be run by passing a valid recipe_file on the command line.

```bash
$ auto_rxn run <recipe_file> --rxn_name "my cool reaction"
```

The `rxn_name` parameter is optional.

## integrating hardware

`auto_rxn` has built-in hardware support for a few models of hardware, under the package `auto_rxn.hardware`.
Beyond this, `auto_rxn` supports the Bluesky Hardware protocol standard.

## recipe files

must have metadata:
- `Control Point ID` (e.g. auto_rxn:FakeMFC)

optional metadata
- control point name
