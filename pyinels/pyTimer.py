"""Inels timer."""
from time import time


class TimerError(Exception):
    """A custom exception used to report errors in use of Timer class"""


class pyTimer:
    """class pyTimer."""

    def __init__(self):
        """Initialize Timer."""
        self.__tick = None
        self.__elapsed_time = None
        self.__stop_after = None
        self.__start_time = None

    @property
    def tick(self):
        """Timer tick property"""
        return self.__tick

    @property
    def is_running(self):
        """Timer is running."""
        return self.__tick is not None

    @property
    def elapsed_time(self):
        """Time to stop timer."""
        return self.__elapsed_time

    def start(self, stop_after):
        """Start a new timer."""
        if self.__start_time is not None:
            # maybee only return void because its running
            raise TimerError("Timer is running. Use .stop() to stop it")

        self.__stop_after = stop_after

        self.__start_time = time()
        self.__tick = time() - self.__start_time
        self.__elapsed_time = self.__stop_after - self.__tick

    def update_tick(self):
        """Update tick time."""
        self.__tick = time() - self.__start_time
        self.__elapsed_time = self.__stop_after - self.__tick

    def stop(self):
        """Stop the timer, and report the elapsed time"""
        if self.__tick is None:
            raise TimerError("Timer is not running. Use .start() to start it")

        self.__tick = None
        self.__start_time = None
        self.__stop_after = None
        self.__elapsed_time = None
