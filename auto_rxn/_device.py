__all__ = ["load_device"]


import pathlib
from typing import Dict, Any, Union
import types

import platformdirs
import happi  # type: ignore
import numpy as np
from bluesky import protocols

from ._limits import Limits


# make happi client
db_path = platformdirs.user_data_path("happi") / "db.json"
happi_backend = happi.backends.backend(db_path)
happi_client = happi.Client(database=happi_backend)


# singleton container for root devices
device_singletons: Dict["str", Any] = dict()


def load_device(id) -> Any:
    """Load a device via happi, monkeypatching as needed."""
    if id in device_singletons:
        return device_singletons[id]
    elif "." in id:
        chain = id.split(".")
        root = chain.pop(0)
        if root in device_singletons:
            device = device_singletons[root]
        else:
            device = happi_client.load_device(name=root)
            device_singletons[root] = device
        while chain:
            device = getattr(device, chain.pop(0))
        return device
    else:
        # grab device from happi
        device = happi_client.load_device(name=id)
        item = happi_client.find_item(name=id)
        setattr(device, "_happi_item", item)
        # finish
        item.save()
        device_singletons[id] = device
        return device
