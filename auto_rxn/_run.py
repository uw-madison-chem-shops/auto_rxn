__all__ = ["run"]


import functools
import pathlib

import bluesky
from bluesky.callbacks.best_effort import BestEffortCallback
from suitcase.csv import Serializer  # type: ignore


def run(recipe):
    from ._happi import happi_client

    devices = dict()
    for id in recipe.control_point_ids:
        device = happi_client.load_device(name=id)
        devices[id] = device
    all_devices = list(devices.values())

    def plan():
        @bluesky.preprocessors.stage_decorator(all_devices)
        @bluesky.preprocessors.run_decorator()
        def inner_plan():
            for step in recipe.steps:
                for id, val in step.setpoints.items():
                    yield from bluesky.plan_stubs.mv(devices[id], float(val))
                yield from bluesky.plan_stubs.repeat(
                    functools.partial(bluesky.plan_stubs.one_shot, all_devices),
                    num=int(float(step.length) * 60),
                    delay=1,
                )

        return (yield from inner_plan())

    RE = bluesky.RunEngine()
    bec = BestEffortCallback()
    bec.disable_plots()
    RE.subscribe(bec)
    RE.subscribe(Serializer("~/auto-rxn-data/", flush=True))
    RE(plan())
