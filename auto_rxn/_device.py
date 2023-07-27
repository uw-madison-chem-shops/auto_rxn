__all__ = ["load_device"]


import appdirs  # type: ignore
import pathlib
import happi  # type: ignore
import numpy as np


# make happi client
db_path = pathlib.Path(appdirs.user_data_dir("happi")) / "db.json"
happi_backend = happi.backends.backend(db_path)
happi_client = happi.Client(database=happi_backend)


# singleton container
device_singletons = dict()


def load_device(id):
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
                    lower, item.auto_rxn_lower_safety_limit
                )
                item.auto_rxn_upper_safety_limit = np.nanmin(
                    upper, item.auto_rxn_upper_safety_limit
                )
        # finish
        item.save()
        device_singletons[id] = device
        return device
