#
# _log.py - DeGirum Python SDK: log functionality
# Copyright DeGirum Corp. 2022
#
# Implements common DeGirum logging functionality
#

import logging
import functools
import time
from contextlib import contextmanager

logger = logging.getLogger(__name__)


class DGLog:
    """Console logging class with programmable verbosity."""

    def __dir__(self):
        return ["set_verbose_state", "print"]

    _prefix = ""
    _suppress = False

    @staticmethod
    def set_verbose_state(state: bool):
        """Set log verbosity state.

        Args:
            state: If `True`, then log prints messages to console, otherwise no messages printed.
        """
        DGLog._suppress = not state

    @staticmethod
    def print(message: str):
        """Print message to log according to current verbosity level.

        Args:
            message: Message string to print.
        """
        if not DGLog._suppress:
            print(DGLog._prefix + message)


def log_wrap(f=None, *, log_level: int = logging.DEBUG):
    """Decorator to log function entry and exit.

    Args:
        f (Callable): Function to log.
        log_level: Logging level of the log entries.
    """
    if f is None:
        return functools.partial(log_wrap, log_level=log_level)

    @functools.wraps(f)
    def wrap(*args, **kwargs):
        t1 = time.time_ns()
        try:
            logger.log(log_level, f"/ {f.__qualname__}")
            return f(*args, **kwargs)
        finally:
            t2 = time.time_ns()
            logger.log(log_level, f"\\ {f.__qualname__} {(t2 - t1) * 1e-3}us ")

    return wrap
