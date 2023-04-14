__all__ = ["Reading"]


from typing import TypedDict


class Reading(TypedDict):
    value: float
    timestamp: float
    alarm_severity: int
    message: str
