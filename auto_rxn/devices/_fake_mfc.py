__all__ = ["FakeMFC", "FakeMFCItem"]


import copy

from happi.item import HappiItem, EntryInfo  # type: ignore

from ._reading import Reading
from ._status import Status


class FakeMFC:
    def __init__(self, name: str):
        self.name = name

    def describe(self) -> dict:
        raise NotImplementedError

    def read(self) -> Reading:
        raise NotImplementedError

    def set(self, value) -> Status:
        raise NotImplementedError


class FakeMFCItem(HappiItem):
    kwargs = copy.copy(HappiItem.kwargs)
    kwargs.default = {"name": "{{name}}"}
    device_class = EntryInfo(default="auto_rxn.devices.FakeMFC")
