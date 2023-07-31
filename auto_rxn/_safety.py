__all__ = ["SafetyCallback"]


import functools


class SafetyCallback(object):
    def __init__(self, devices: dict):
        self.devices = devices
        self.current_step = None
        self.i = 0

    def __call__(self, name, document):
        """Consumes the document stream."""
        if "data" not in document:
            return
        data = document["data"]
        for name, device in self.devices.items():
            if "." in name:
                continue
            keys = ["_".join([name, suffix]) for suffix in ["setpoint", "readback", "destination"]]
            keys.append(name)
            for key in keys:
                if key not in data:
                    continue
                if device._happi_item["auto_rxn_lower_safety_limit"] is not None:
                    if data[key] < device._happi_item["auto_rxn_lower_safety_limit"]:
                        print(f"{name} went below safety limit!")
                        raise Exception
                if device._happi_item["auto_rxn_upper_safety_limit"] is not None:
                    if data[key] > device._happi_item["auto_rxn_upper_safety_limit"]:
                        print(f"{name} went above safety limit!")
                        raise Exception
