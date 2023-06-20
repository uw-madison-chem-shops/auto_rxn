__all__ = ["FakeMFC", "FakeMFCItem"]


import copy
import time
import threading
from typing import Dict

from happi.item import HappiItem, EntryInfo  # type: ignore

from ._reading import Reading
from ._status import Status


class FakeMFC:
    def __init__(self, name: str):
        self.name = name
        self.parent = None
        self.value = 0.0

    def describe(self) -> dict:
        out = dict()
        out[f"{self.name}_setpoint"] = {"source": "FakeMFC", "dtype": "number", "shape": []}
        out[f"{self.name}_readback"] = {"source": "FakeMFC", "dtype": "number", "shape": []}
        return out

    def read(self) -> dict:
        ts = time.time()
        out = dict()
        out[f"{self.name}_setpoint"] = {"value": self.value, "timestamp": ts}
        out[f"{self.name}_readback"] = {"value": self.value, "timestamp": ts}
        return out

    def set(self, value) -> Status:
        self.value = value
        st = Status()

        def done_later():
            time.sleep(0.1)
            st.set_finished()

        threading.Thread(target=done_later).start()

        return st


class FakeMFCItem(HappiItem):
    kwargs = copy.copy(HappiItem.kwargs)
    kwargs.default = {"name": "{{name}}"}
    device_class = EntryInfo(default="auto_rxn.devices.FakeMFC")
