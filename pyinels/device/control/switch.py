"""Switch control class."""
import logging

_LOGGER = logging.getLogger(__name__)


class SwitchControl:
    """Switch control class."""

    def __init__(self, device, api):
        """Initialize switch control class."""
        super().__init__(self, device, api)

    @property
    def toggle(self):
        """Toogle the state of the switch."""
        new_state = True if self.__device.state is False else False

        self.__device.set_value(1 if new_state is True else 0)
