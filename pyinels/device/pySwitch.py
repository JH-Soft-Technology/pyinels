"""Inels switch class for iNels BUS."""

from pyinels.const import (
    ATTR_SWITCH_ON
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

    def turn_off(self):
        """Turn the switch off."""
        self.__device.set_value(0)

    def turn_on(self):
        """Turn the switch on."""
        self.__device.set_value(1)

    def __repr__(self):
        """Object representation."""
        state = "on" if self.state else "off"
        return "<Switch #{} - " \
            "title: {}, " \
            "state: {}" \
            ">".format(self.__device.id, self.__device.title, state)
