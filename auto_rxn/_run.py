__all__ = ["run"]


import functools
import pathlib
import itertools

import bluesky
from bluesky.callbacks.best_effort import BestEffortCallback
from bluesky.utils import RequestStop
from suitcase.csv import Serializer  # type: ignore
import numpy as np

from ._device import load_device
from ._safety import SafetyCallback


def run(recipe):
    RE = bluesky.RunEngine()

    devices = dict()
    for id in recipe.control_point_ids:
        devices[id] = load_device(id)
    all_devices = list(devices.values())

    bec = BestEffortCallback()
    bec.disable_plots()
    RE.subscribe(bec)

    RE.subscribe(Serializer("~/auto-rxn-data/", flush=True))

    safety = SafetyCallback(devices)
    RE.subscribe(safety, "all")

    def plan():
        @bluesky.preprocessors.stage_decorator(all_devices)
        @bluesky.preprocessors.run_decorator()
        def inner_plan():
            for step in recipe.steps:
                nestargs = [(devices[id], float(val)) for id, val in step.setpoints.items()]
                yield from bluesky.plan_stubs.mv(*itertools.chain(*nestargs))

                def fallback_to_safety(exception):
                    # set to most recent known good position (currently all zero... todo)
                    nestargs = [(devices[id], 0.0) for id, val in step.setpoints.items()]
                    yield from bluesky.plan_stubs.mv(*itertools.chain(*nestargs))
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

    RE(plan())
