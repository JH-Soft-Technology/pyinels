"""Inels timer."""
from time import time


class TimerError(Exception):
    """A custom exception used to report errors in use of Timer class"""


class Timer:
    def __init__(self):
        self._tick = None
        self._elapsed_time = None
        self._direction = None
        self._start_time = None

    @property
    def tick(self):
        """Timer tick property"""
        return self._tick

    def start(self, direction):
        """Start a new timer with direction"""
        if self._start_time is not None:
            # maybee only return void because its running
            raise TimerError("Timer is running. Use .stop() to stop it")

        self._start_time = time()
        self._tick = time() - self._start_time
        self._direction = direction

    def update_tick(self):
        """Update tick time."""
        self._tick = time() - self._start_time
        self._elapsed_time = None

    def stop(self):
        """Stop the timer, and report the elapsed time"""
        if self._start_time is None:
            raise TimerError("Timer is not running. Use .start() to start it")

        self._tick = None
        self._start_time = None
        self._direction = None
