__all__ = ["SafetyCallback"]


import functools


class SafetyCallback(object):
    def __init__(self, devices):
        self.devices = devices
        self.current_step = None
        self.i = 0

    def __call__(self, name, document):
        """Consumes the document stream."""
        self.i += 1
        if self.i == 6:
            raise Exception
