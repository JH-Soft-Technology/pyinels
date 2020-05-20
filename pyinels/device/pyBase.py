"""Inels base class for iNels BUS devices."""

from pyinels.const import (
    ATTR_SWITCH_ON,
    ATTR_SWITCH_OFF
)


class pyBase:
    """Inels base class."""

    def __init__(self, device):
        """Initialize object."""
        self._device = device
        self._device.observe()

    @property
    def state(self):
        """Return the state of the switch."""
        return (True if self._device.value
                == ATTR_SWITCH_ON else False)

    @property
    def name(self):
        """Name of the light."""
        return self._device.title

    @property
    def unique_id(self):
        """Unique id of the device."""
        return self._device.id

    def turn_off(self):
        """Turn the switch off."""
        self._device.write_value(ATTR_SWITCH_OFF)

    def turn_on(self):
        """Turn the switch on."""
        self._device.write_value(ATTR_SWITCH_ON)

    def update(self):
        """Update data on the device."""
        return self._device.observe()

    def __repr__(self):
        """Object representation."""
        state = "on" if self.state else "off"
        return "<{} #{} - " \
            "title: {}, " \
            "state: {}" \
            ">".format(self._device.type, self._device.id,
                       self._device.title, state)
