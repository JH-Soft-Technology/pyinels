"""Unit testing of timer library."""

from unittest import TestCase
from pyinels.pyTimer import pyTimer


class PyTimerTest(TestCase):
    """Class to test timer library."""

    def setUp(self):
        """Setup pyTimer for testing."""
        self.timer = pyTimer()

    def tearDown(self):
        """Dealloc all properties defined in setup."""
        self.timer = None

    def test_initialize_timer(self):
        """Test of pyTimer initialization."""

        self.assertIsNone(self.timer.tick)
        self.assertIsNone(self.timer.elapsed_time)
        self.assertFalse(self.timer.is_running)

    def test_start_timer(self):
        """Start the timer test."""

        self.timer.start(2)

        self.assertTrue(self.timer.is_running)
        self.assertIsNotNone(self.timer.tick)
        self.assertIsNotNone(self.timer.elapsed_time)

        self.assertLess(self.timer.tick, self.timer.elapsed_time)

    def test_stop_timer(self):
        """Stop the timer test."""

        self.timer.start(2)

        self.assertTrue(self.timer.is_running)
        self.assertIsNotNone(self.timer.elapsed_time)
        self.assertIsNotNone(self.timer.tick)

        self.timer.stop()

        self.assertIsNone(self.timer.tick)
        self.assertIsNone(self.timer.elapsed_time)
        self.assertFalse(self.timer.is_running)
