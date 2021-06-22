"""Inels light class for iNels BUS."""

from pyinels.device.pyBase import pyBase

from pyinels.const import (
    RANGE_BRIGHTNESS,
    ATTR_SWITCH_ON,
    ATTR_SWITCH_OFF
)

MIN_RANGE = RANGE_BRIGHTNESS[0]
MAX_RANGE = RANGE_BRIGHTNESS[1]


class pyLight(pyBase):
    """Inels class based on InelsDevice."""

    def __init__(self, device):
        """Initialize object."""
        super().__init__(device)
        self.__has_brightness = isinstance(self.value, float)

    @property
    def state(self):
        """State of the light."""
        if self.has_brightness:
            return (True if self.value
                    > MIN_RANGE else False)

        return (True if self.value
                == ATTR_SWITCH_ON else False)

    @property
    def has_brightness(self):
        """Supports brightness."""
        return self.__has_brightness

    def set_brightness(self, value):
        """Set brightness of the light."""
        if (self.has_brightness
                and (value >= MIN_RANGE and value <= MAX_RANGE)):
            self._device.write_value(value)

    def brightness(self):
        """Return the brightness value."""
        if self.has_brightness is True:
            return self.value

        return None

    def turn_off(self):
        """Turn off the light."""
        if self.has_brightness is True:
            self._device.write_value(MIN_RANGE)
            return

        self._device.write_value(ATTR_SWITCH_OFF)

    def turn_on(self):
        """Turn on the light."""
        if self.has_brightness is True:
            self._device.write_value(MAX_RANGE)
        else:
            # set device value to 0 when turn off and to 1 when turn on
            self._device.write_value(ATTR_SWITCH_ON)
