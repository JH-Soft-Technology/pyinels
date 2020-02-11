"""Inels switch class for iNels BUS."""

from inels.const import (
    ATTR_SWITCH_ON
)


class InelsSwitch:
    """Switch class based on InelsDevice."""

    def __init__(self, device):
        """Initialize of object InelsSwitch."""
        self.device = device

    @property
    def state(self):
        """Return the state of the switch."""
        if (self.device.value is None):
            self.device.observe()

        val = str(self.device.value)
        attr = ATTR_SWITCH_ON

        # it is expression of ternary operator
        return (True if val == attr else False)

    def toggle(self):
        """Toogle the state of the switch."""
        new_state = True if self.state is False else False

        self.device.set_value(1 if new_state is True else 0)
