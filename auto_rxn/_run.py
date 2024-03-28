__all__ = ["run"]


import os
import functools
import pathlib
import itertools
import datetime
import shutil

import tomli
import platformdirs
import bluesky
from bluesky.callbacks.best_effort import BestEffortCallback
from bluesky.utils import RequestStop
from suitcase.csv import Serializer  # type: ignore
import numpy as np

from ._device import load_device
from ._limits import LimitsChecker, limits

from . import _stage_unstage as su


def run(recipe):
    RE = bluesky.RunEngine()

    path = platformdirs.user_config_path("auto-rxn") / "config.toml"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch(exist_ok=True)
    with open(path, "rb") as f:
        config = tomli.load(f)

    devices = dict()
    for id in recipe.control_point_ids:
        devices[id] = load_device(id)
    all_devices = list(devices.values())

    if "streams" in config:
        if "primary" in config["streams"]:
            if "devices" in config["streams"]["primary"]:
                for id in config["streams"]["primary"]["devices"]:
                    if id in recipe.control_point_ids:
                        continue
                    all_devices.append(load_device(id))

    bec = BestEffortCallback()
    bec.disable_plots()
    RE.subscribe(bec)

    datadir = os.path.expanduser("~")
    datadir += os.sep + "auto-rxn-data"
    datadir += os.sep + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    datadir = pathlib.Path(datadir)
    datadir.mkdir(exist_ok=True, parents=True)
    RE.subscribe(Serializer(datadir, flush=True))
    recipe.save(datadir / "recipe.csv")
    from ._device import db_path

    shutil.copyfile(db_path, datadir / "db.json")

    limits.save(datadir / "limits.toml")

    safety = LimitsChecker(devices)
    safety_token = RE.subscribe(safety, "all")

    def plan():
        @bluesky.preprocessors.stage_decorator(all_devices)
        @bluesky.preprocessors.run_decorator()
        def inner_plan():
            for step, fallback_positions in zip(recipe.steps, recipe.fallback_positions):
                # set fallback positions
                for id, val in fallback_positions.setpoints.items():
                    limits.set_fallback(id, val)

                # set positions
                for id, val in step.setpoints.items():
                    yield from bluesky.plan_stubs.abs_set(devices[id], val)

                def fallback_to_safety(exception):
                    print(exception)
                    print("recovering to fallback positions")
                    RE.unsubscribe(safety_token)  # don't want to keep raising
                    for name, device in devices.items():
                        fallback = limits.get_fallback(name)
                        try:
                            if not np.isnan(fallback):
                                yield from bluesky.plan_stubs.abs_set(device, fallback)
                        except TypeError:  # fallback is a string, probably
                            yield from bluesky.plan_stubs.abs_set(device, fallback)
                    # keep recording data for 100 more seconds
                    yield from bluesky.plan_stubs.repeat(
                        functools.partial(bluesky.plan_stubs.one_shot, all_devices),
                        num=int(100),
                        delay=1,
                    )
                    raise RequestStop

                @bluesky.preprocessors.contingency_decorator(except_plan=fallback_to_safety)
                def count_until_next_set():
                    yield from bluesky.plan_stubs.repeat(
                        functools.partial(bluesky.plan_stubs.one_shot, all_devices),
                        num=int(float(step.length) * 60),
                        delay=1,
                    )

                yield from count_until_next_set()

        return (yield from inner_plan())

    su.stage(recipe, RE, devices, datadir)
    RE(plan())
    su.unstage(recipe, RE, devices, datadir)
