__all__ = ["FakeFurnace", "FakeFurnaceItem"]


import copy

from happi.item import HappiItem, EntryInfo  # type: ignore

from ._reading import Reading
from ._status import Status


class FakeFurnace:
    def __init__(self, name: str):
        self.name = name

    def describe(self) -> dict:
        raise NotImplementedError

    def read(self) -> Reading:
        raise NotImplementedError

    def set(self, value) -> Status:
        raise NotImplementedError


class FakeFurnaceItem(HappiItem):
    kwargs = copy.copy(HappiItem.kwargs)
    kwargs.default = {"name": "{{name}}"}
    device_class = EntryInfo(default="auto_rxn.devices.FakeFurnace")
