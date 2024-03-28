#!/usr/bin/env python3

import click
import platformdirs
import sys
import subprocess
import os
import tomli


from ._device import happi_client
from .__version__ import __version__
from ._recipe import Recipe
from ._run import run
from ._limits import limits
from ._stage_unstage import script_path


@click.group()
@click.version_option(__version__)
def main():
    pass


@main.command(name="edit-config")
def edit_config():
    path = platformdirs.user_config_path("auto-rxn") / "config.toml"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch(exist_ok=True)

    while True:
        if sys.platform.startswith("win32"):
            subprocess.run([os.environ.get("EDITOR", "notepad.exe"), str(path)])
        else:
            subprocess.run([os.environ.get("EDITOR", "vi"), path])
        try:
            with open(path, "rb") as f:
                tomli.load(f)
            break
        except Exception as e:
            print(e, file=sys.stderr)

            if not click.confirm(
                "Error parsing config toml. Would you like to re-edit?",
                default=True,
            ):
                break


@main.command(name="edit-limits")
def _edit_limits():
    path = platformdirs.user_data_path("auto-rxn") / "limits.toml"
    if sys.platform.startswith("win32"):
        import shutil

        editor = shutil.which(os.environ.get("EDITOR", "notepad.exe"))
        subprocess.run([editor, str(path)])
    else:
        subprocess.run([os.environ.get("EDITOR", "vi"), str(path)])


@main.command(name="edit-stage-unstage")
def _edit_stage_unstage():
    if sys.platform.startswith("win32"):
        import shutil

        editor = shutil.which(os.environ.get("EDITOR", "notepad.exe"))
        subprocess.run([editor, str(script_path)])
    else:
        subprocess.run([os.environ.get("EDITOR", "vi"), str(script_path)])


@main.command(name="list-devices")
def _list_devices():
    def print_all_limits(control_id):
        print(f"    atol: {limits.get_atol(control_id)}")
        print(f"    deadband: {limits.get_deadband(control_id)}")
        print(f"    delay (s): {limits.get_delay(control_id)}")
        print(f"    fallback: {limits.get_fallback(control_id)}")
        print(f"    lower: {limits.get_lower(control_id)}")
        print(f"    rtol (%): {limits.get_rtol(control_id)}")
        print(f"    upper: {limits.get_upper(control_id)}")

    for name, result in happi_client.items():
        print(name)
        print(f"    device_class: {result.metadata['device_class']}")
        print_all_limits(name)
        for other in limits._state.keys():
            if other.startswith(f"{name}."):
                print(other)
                print_all_limits(other)


@main.command(name="run")
@click.argument("recipe", type=click.Path())
def _run(recipe):
    r = Recipe(recipe)
    run(r)
