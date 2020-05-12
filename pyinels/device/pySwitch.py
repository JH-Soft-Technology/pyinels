"""Inels switch class for iNels BUS."""

from pyinels.const import (
    ATTR_SWITCH_ON,
    ATTR_SWITCH_OFF
)


class pySwitch:
    """Switch class based on InelsDevice."""

    def __init__(self, device):
        """Initialize of object InelsSwitch."""
        self.__device = device

    @property
    def state(self):
        """Return the state of the switch."""
        if (self.__device.value is None):
            self.__device.observe()

        val = str(self.__device.value)
        attr = ATTR_SWITCH_ON

        # it is expression of ternary operator
        return (True if val == attr else False)

    @property
    def name(self):
        """Name of the device."""
        return self.__device.title

    @property
    def unique_id(self):
        """Unique id of the device."""
        return self.__device.id

    def turn_off(self):
        """Turn the switch off."""
        self.__device.set_value(ATTR_SWITCH_OFF)

    def turn_on(self):
        """Turn the switch on."""
        self.__device.set_value(ATTR_SWITCH_ON)

    def __repr__(self):
        """Object representation."""
        state = "on" if self.state else "off"
        return "<Switch #{} - " \
            "title: {}, " \
            "state: {}" \
            ">".format(self.__device.id, self.__device.title, state)
