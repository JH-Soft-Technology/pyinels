"""Inels light class for iNels BUS."""

from inels.const import (
    RANGE_BRIGHTNESS
)

MIN_RANGE = RANGE_BRIGHTNESS[0]
MAX_RANGE = RANGE_BRIGHTNESS[1]


class InelsLight:
    """Inels class based on InelsDevice."""

    def __init__(self, device):
        """Initialize object."""
        self.device = device

    @property
    def state(self):
        """State of the light."""
        if self.device.value is None:
            self.device.observe()

        return True if self.device.value > 0 else False

    @property
    def has_brightness(self):
        """Supports brightness."""
        if self.device.value is None:
            self.device.observe()

        return isinstance(self.device.value, float)

    def set_brightness(self, value):
        """Set brightness of the light."""
        if (self.has_brightness
                and (value > MIN_RANGE and value <= MAX_RANGE)):
            self.device.set_value(value)

    def set_state(self):
        """Toogle state which will be turn on or off the light."""
        if self.has_brightness is True:
            # when the light has brightness then set max range for turn on
            # and min range for turn off
            self.device.set_value(
                MIN_RANGE if self.state is True else MAX_RANGE)
        else:
            # set device value to 0 when turn off and to 1 when turn on
            self.device.set_value(1 if self.state is False else 0)
