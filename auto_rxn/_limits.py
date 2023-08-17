__all__ = ["limits", "LimitsChecker"]


import time
from typing import Dict

import numpy as np
import platformdirs
import tomli
import tomli_w


class Limits(object):
    _instance = None

    def __init__(self):
        self._path = platformdirs.user_data_path("auto-rxn") / "limits.toml"
        self._path.parent.mkdir(exist_ok=True, parents=True)
        self._path.touch(exist_ok=True)
        with open(self._path, "rb") as f:
            self._state = tomli.load(f)

    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance

    def _get(self, control_id, key):
        return self._state[control_id][key]

    def get_atol(self, control_id):
        try:
            return self._get(control_id, "atol")
        except KeyError:
            self._set(control_id, "atol", float("+inf"))
        return self._get(control_id, "atol")

    def get_deadband(self, control_id):
        try:
            return self._get(control_id, "deadband")
        except KeyError:
            self._set(control_id, "deadband", 0.0)
        return self._get(control_id, "deadband")

    def get_delay(self, control_id):
        try:
            return self._get(control_id, "delay")
        except KeyError:
            self._set(control_id, "delay", 0.0)
        return self._get(control_id, "delay")

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

    def get_rtol(self, control_id):
        try:
            return self._get(control_id, "rtol")
        except KeyError:
            self._set(control_id, "rtol", float("+inf"))
        return self._get(control_id, "rtol")

    def get_upper(self, control_id):
        try:
            return self._get(control_id, "upper")
        except KeyError:
            self._set(control_id, "upper", float("+inf"))
        return self._get(control_id, "upper")

    def save(self, path):
        with open(path, "wb") as f:
            tomli_w.dump(self._state, f)

    def _set(self, control_id, key, value):
        if control_id not in self._state:
            self._state[control_id] = dict()
        self._state[control_id][key] = value
        self.save(self._path)

    def set_atol(self, control_id, value):
        assert value >= 0
        return self._set(control_id, "atol", value)

    def set_deadband(self, control_id, value):
        assert value >= 0
        return self._set(control_id, "deadband", value)

    def set_delay(self, control_id, value):
        assert value >= 0
        return self._set(control_id, "delay", value)

    def set_fallback(self, control_id, value):
        return self._set(control_id, "fallback", value)

    def set_lower(self, control_id, value):
        return self._set(control_id, "lower", value)

    def set_rtol(self, control_id, value):
        assert value >= 0
        return self._set(control_id, "rtol", value)

    def set_upper(self, control_id, value):
        return self._set(control_id, "upper", value)


limits = Limits()


class LimitsChecker(object):
    def __init__(self, devices: dict):
        self.devices = devices
        self.current_step = None
        self.i = 0
        self.last_pass: Dict[str, float] = dict()
        self.fail_cache: Dict[str, str] = dict()

    def __call__(self, name, document):
        """Consumes the document stream."""
        now = time.time()
        if "data" not in document:
            return
        data = document["data"]
        for name, device in self.devices.items():
            if f"{name}_setpoint" in data:
                setpoint = data[f"{name}_setpoint"]
            else:
                setpoint = data.get(f"{name}_destination", np.nan)
            if f"{name}_readback" in data:
                readback = data[f"{name}_readback"]
            else:
                readback = data.get(name, np.nan)
            # if we're operating with discrete data, always pass
            if isinstance(setpoint, str):
                self.last_pass[name] = time.time()
                continue
            if isinstance(readback, str):
                self.last_pass[name] = time.time()
                continue
            # if you're inside the deadband, always pass
            deadband = limits.get_deadband(name)
            if (0 - deadband) < setpoint < (0 + deadband):
                if (0 - deadband) < readback < (0 + deadband):
                    self.last_pass[name] = time.time()
                    continue
            # limits apply to setpoint and readback
            if setpoint < limits.get_lower(name):
                self.fail_cache[name] = f"{name} went below safety limit!"
                continue
            if readback < limits.get_lower(name):
                self.fail_cache[name] = f"{name} went below safety limit!"
                continue
            if setpoint > limits.get_upper(name):
                self.fail_cache[name] = f"{name} went above safety limit!"
                continue
            if readback > limits.get_upper(name):
                self.fail_cache[name] = f"{name} went above safety limit!"
                continue
            # atol
            if np.abs(setpoint - readback) > limits.get_atol(name):
                self.fail_cache[name] = f"{name} went outside of absolute tolerance"
                continue
            # rtol
            if np.abs(setpoint - 0.0) > 1e-6:
                if np.abs((setpoint - readback) / setpoint) * 100 > limits.get_rtol(name):
                    self.fail_cache[name] = f"{name} went outside of relative tolerance"
                    continue
            self.last_pass[name] = time.time()
        for name, device in self.devices.items():
            keys = ["_".join([name, suffix]) for suffix in ["setpoint", "readback", "destination"]]
            keys.append(name)
            for key in keys:
                if key not in data:
                    continue
                if now - self.last_pass[name] > limits.get_delay(name):
                    raise Exception(self.fail_cache[name])
