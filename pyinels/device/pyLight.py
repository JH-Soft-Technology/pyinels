"""Inels light class for iNels BUS."""

from pyinels.const import (
    RANGE_BRIGHTNESS
)

MIN_RANGE = RANGE_BRIGHTNESS[0]
MAX_RANGE = RANGE_BRIGHTNESS[1]


class pyLight:
    """Inels class based on InelsDevice."""

    def __init__(self, device):
        """Initialize object."""
        self.__device = device

    @property
    def state(self):
        """State of the light."""
        if self.__device.value is None:
            self.__device.observe()

        return True if self.__device.value > 0 else False

    @property
    def name(self):
        """Name of the light."""
        return self.__device.title

    @property
    def unique_id(self):
        """Unique id of the device."""
        return self.__device.id

    @property
    def has_brightness(self):
        """Supports brightness."""
        if self.__device.value is None:
            self.__device.observe()

        return isinstance(self.__device.value, float)

    def set_brightness(self, value):
        """Set brightness of the light."""
        if (self.has_brightness
                and (value > MIN_RANGE and value <= MAX_RANGE)):
            self.__device.set_value(value)

    def turn_off(self):
        """Turn off the light."""
        self.__device.set_value(0)

    def turn_on(self):
        """Turn on the light."""
        if self.has_brightness is True:
            # when the light has brightness then set max range for turn on
            # and min range for turn off
            self.__device.set_value(
                MIN_RANGE if self.state is True else MAX_RANGE)
        else:
            # set device value to 0 when turn off and to 1 when turn on
            self.__device.set_value(1)
