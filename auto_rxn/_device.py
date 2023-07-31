__all__ = ["load_device"]


import pathlib
from typing import Dict, Any, Union
import types

import appdirs  # type: ignore
import happi  # type: ignore
import numpy as np
from bluesky import protocols


# make happi client
db_path = pathlib.Path(appdirs.user_data_dir("happi")) / "db.json"
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
        # limits
        if not "auto_rxn_lower_safety_limit" in item.keys():
            item.info_names.append("auto_rxn_lower_safety_limit")
            item.auto_rxn_lower_safety_limit = None
        if not "auto_rxn_upper_safety_limit" in item.keys():
            item.info_names.append("auto_rxn_upper_safety_limit")
            item.auto_rxn_upper_safety_limit = None
        if hasattr(device, "yaq_traits"):
            if "has-limits" in device.yaq_traits:
                lower, upper = device.yaq_client.get_limits()
                item.auto_rxn_lower_safety_limit = np.nanmax(
                    [lower, item["auto_rxn_lower_safety_limit"]]
                )
                item.auto_rxn_upper_safety_limit = np.nanmin(
                    [upper, item["auto_rxn_upper_safety_limit"]]
                )
        # fallback position

        def get_fallback_position(self) -> Union[float, None]:
            return self._happi_item["auto_rxn_fallback_position"]

        def set_fallback_position(self, position: Union[float, None]):
            self._happi_item.auto_rxn_fallback_position = position
            self._happi_item.save()

        device.get_fallback_position = types.MethodType(get_fallback_position, device)
        device.set_fallback_position = types.MethodType(set_fallback_position, device)
        if not "auto_rxn_fallback_position" in item.keys():
            item.info_names.append("auto_rxn_fallback_position")
            item.auto_rxn_fallback_position = None
        # finish
        item.save()
        device_singletons[id] = device
        return device
