__all__ = ["FakeFurnace", "FakeFurnaceItem"]


import copy
import time

from happi.item import HappiItem, EntryInfo  # type: ignore

from ._reading import Reading
from ._status import Status


class FakeFurnace:
    def __init__(self, name: str):
        self.name = name
        self.parent = None
        self.value = 0.0

    def describe(self) -> dict:
        out = dict()
        out[f"{self.name}_setpoint"] = {"source": "FakeFurnace", "dtype": "number", "shape": []}
        out[f"{self.name}_readback"] = {"source": "FakeFurnace", "dtype": "number", "shape": []}
        return out

    def read(self) -> dict:
        ts = time.time()
        out = dict()
        out[f"{self.name}_setpoint"] = {"value": self.value, "timestamp": ts}
        out[f"{self.name}_readback"] = {"value": self.value, "timestamp": ts}
        return out

    def set(self, value) -> Status:
        self.value = value
        s = Status()
        s.set_finished()
        return s


class FakeFurnaceItem(HappiItem):
    kwargs = copy.copy(HappiItem.kwargs)
    kwargs.default = {"name": "{{name}}"}
    device_class = EntryInfo(default="auto_rxn.devices.FakeFurnace")
