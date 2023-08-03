__all__ = ["limits", "LimitsChecker"]


import numpy as np
import platformdirs
import tomli
import tomli_w


class Limits(object):
    _instance = None

    def __init__(self):
        self._path = platformdirs.user_data_path("auto-rxn") / "limits.toml"
        self._path.parent.mkdir(exist_ok=True)
        self._path.touch(exist_ok=True)
        with open(self._path, "rb") as f:
            self._state = tomli.load(f)

    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance

    def _get(self, control_id, key):
        return self._state[control_id][key]

    def get_fallback(self, control_id):
        try:
            return self._get(control_id, "fallback")
        except KeyError:
            self._set(control_id, "fallback", float("nan"))
        return self._get(control_id, "fallback")

    def get_lower(self, control_id):
        try:
            return self._get(control_id, "lower")
        except KeyError:
            self._set(control_id, "lower", float("-inf"))
        return self._get(control_id, "lower")

    def get_upper(self, control_id):
        try:
            return self._get(control_id, "upper")
        except KeyError:
            self._set(control_id, "upper", float("+inf"))
        return self._get(control_id, "upper")

    def _set(self, control_id, key, value):
        if control_id not in self._state:
            self._state[control_id] = dict()
        self._state[control_id][key] = value
        with open(self._path, "wb") as f:
            tomli_w.dump(self._state, f)

    def set_fallback(self, control_id, value):
        return self._set(control_id, "fallback", value)

    def set_lower(self, control_id, value):
        return self._set(control_id, "lower", value)

    def set_upper(self, control_id, value):
        return self._set(control_id, "upper", value)


limits = Limits()


class LimitsChecker(object):
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
            keys = ["_".join([name, suffix]) for suffix in ["setpoint", "readback", "destination"]]
            keys.append(name)
            for key in keys:
                if key not in data:
                    continue
                if data[key] < limits.get_lower(name):
                    raise Exception(f"{name} went below safety limit!")
                if data[key] > limits.get_upper(name):
                    raise Exception(f"{name} went above safety limit ({limits.get_upper(name)})!")
