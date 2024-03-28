import importlib.util
import platformdirs
import pathlib
from typing import List

import numpy as np
import bluesky
from bluesky import protocols

from ._recipe import Recipe


script_path = platformdirs.user_data_path("auto-rxn") / "stage_unstage.py"


default = """# auto-rxn stage unstage
# the functions below will be called whenever auto-rxn starts or stops a run
# unstage is called no-matter what, even if a run fails or is canceled
# of course, if auto-rxn crashes it won't have a chance to call unstage
# it's not a great idea to try to hold state between stage and unstage
# if you must, use globals...


import pathlib
from typing import List

import numpy as np
import bluesky
from bluesky import protocols
import auto_rxn


def stage(recipe: auto_rxn.Recipe,
          RE: bluesky.RunEngine,
          devices: List[bluesky.protocols.Readable],
          datadir: pathlib.Path,
          *args,
          **kwargs
          ) -> None:
    pass


def unstage(recipe: auto_rxn.Recipe,
            RE: bluesky.RunEngine,
            devices: List[bluesky.protocols.Readable],
            datadir: pathlib.Path,
            *args,
            **kwargs
            ) -> None:
    pass

"""

# put default if not exists
if not script_path.is_file():
    with open(script_path, "w") as f:
        f.write(default)


def _get_module():
    spec = importlib.util.spec_from_file_location(
        script_path.name.removesuffix(script_path.suffix), script_path
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def stage(
    recipe: auto_rxn._recipe.Recipe,
    RE: bluesky.RunEngine,
    devices: List[bluesky.protocols.Readable],
    datadir: pathlib.Path,
    *args,
    **kwargs,
) -> None:
    module = _get_module()
    module.stage(recipe, RE, devices, datadir, *args, **kwargs)


def unstage(
    recipe: auto_rxn._recipe.Recipe,
    RE: bluesky.RunEngine,
    devices: List[bluesky.protocols.Readable],
    datadir: pathlib.Path,
    *args,
    **kwargs,
) -> None:
    module = _get_module()
    module.unstage(recipe, RE, devices, datadir, *args, **kwargs)
