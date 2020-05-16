"""Inels light class for iNels BUS."""

from pyinels.const import (
    RANGE_BRIGHTNESS,
    ATTR_SWITCH_ON,
    ATTR_SWITCH_OFF
)

MIN_RANGE = RANGE_BRIGHTNESS[0]
MAX_RANGE = RANGE_BRIGHTNESS[1]


class pyLight:
    """Inels class based on InelsDevice."""

    def __init__(self, device):
        """Initialize object."""
        self.__device = device
        self.__device.observe()
        self.__has_brightness = isinstance(self.__device.value, float)

    @property
    def state(self):
        """State of the light."""
        self.__device.observe()

        if self.has_brightness:
            return (True if self.__device.value > MIN_RANGE else False)

        val = str(self.__device.value)
        attr = ATTR_SWITCH_ON

        return (True if val == attr else False)

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
        return self.__has_brightness

    def set_brightness(self, value):
        """Set brightness of the light."""
        if (self.has_brightness
                and (value >= MIN_RANGE and value <= MAX_RANGE)):
            self.__device.set_value(value)

    def brightness(self):
        """Return the brightness value."""
        if self.has_brightness is True:
            return self.__device.value

        return None

    def turn_off(self):
        """Turn off the light."""
        if self.has_brightness is True:
            self.__device.set_value(MIN_RANGE)
            return

        self.__device.set_value(ATTR_SWITCH_OFF)

    def turn_on(self):
        """Turn on the light."""
        if self.has_brightness is True:
            # when the light has brightness then set max range for turn on
            # and min range for turn off
            self.__device.set_value(
                MIN_RANGE if self.state is True else MAX_RANGE)
        else:
            # set device value to 0 when turn off and to 1 when turn on
            self.__device.set_value(ATTR_SWITCH_ON)

    def __repr__(self):
        """Object representation."""
        state = "on" if self.state else "off"
        return "<Light #{} - " \
            "title: {}, " \
            "state: {}" \
            ">".format(self.__device.id, self.__device.title, state)
