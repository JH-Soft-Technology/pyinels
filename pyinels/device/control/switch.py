"""Switch control class."""
import logging

_LOGGER = logging.getLogger(__name__)


class SwitchControl:
    """Switch control class."""

    def __init__(self, device):
        """Initialize switch control class."""
        self.__device = device

    @property
    def toggle(self):
        """Toogle the state of the switch."""
        self.__device.set_value(1 if self.__device.value == 0 else 0)
