__all__ = [
    "AutoRxnException",
    "InvalidState",
    "UnknownStatusFailure",
    "StatusTimeoutError",
    "WaitTimeoutError",
]


class AutoRxnException(Exception):
    """
    auto_rxn base exception class
    """

    pass


class InvalidState(RuntimeError, AutoRxnException):
    """
    When Status.set_finished() or Status.set_exception(exc) is called too late
    """

    ...


class UnknownStatusFailure(AutoRxnException):
    """
    Generic error when a Status object is marked success=False without details.
    """

    ...


class StatusTimeoutError(TimeoutError, AutoRxnException):
    """
    Timeout specified when a Status object was created has expired.
    """

    ...


class UseNewProperty(RuntimeError, AutoRxnException):
    ...


class WaitTimeoutError(TimeoutError, AutoRxnException):
    """
    TimeoutError raised when we ware waiting on completion of a task.
    This is distinct from TimeoutError, just as concurrent.futures.TimeoutError
    is distinct from TimeoutError, to differentiate when the task itself has
    raised a TimeoutError.
    """

    ...
