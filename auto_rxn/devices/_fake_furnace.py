__all__ = ["FakeFurnace", "FakeFurnaceItem"]


import copy
import time

from happi.item import HappiItem, EntryInfo  # type: ignore

from ._reading import Reading
from ._status import Status


class PropertyDevice(object):
    def __init__(self, parent, name):
        self.parent = parent
        self.name = name
        self._setpoint = float("nan")
        self._readback = float("nan")

    def set(self, value) -> Status:
        self._setpoint = float(value)
        self._readback = float(value)
        st = Status()
        st.set_finished()
        st.wait()
        return st

    def describe(self) -> dict:
        out = dict()
        out[f"{self.parent.name}_{self.name}_readback"] = {"source": "FakeFurnace", "dtype": "number", "shape": []}
        out[f"{self.parent.name}_{self.name}_setpoint"] = {"source": "FakeFurnace", "dtype": "number", "shape": []}
        return out

    def read(self) -> dict:
        ts = time.time()
        out = dict()
        out[f"{self.parent.name}_{self.name}_readback"] = {
            "value": self._readback,
            "timestamp": ts,
        }
        out[f"{self.parent.name}_{self.name}_setpoint"] = {
            "value": self._setpoint,
            "timestamp": ts,
        }
        return out


class FakeFurnace:
    def __init__(self, name: str):
        self.name = name
        self.parent = None
        self.value = 0.0
        self.ramp_time = PropertyDevice(self, "ramp_time")
        self.children = [self.ramp_time]

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
