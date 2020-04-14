"""Common device class for iNels BUS."""
import logging

from pyinels.api.resources import ApiResource
from pyinels.const import (
    ATTR_SWITCH
)

from pyinels.device.control.switch import SwitchControl

_LOGGER = logging.getLogger(__name__)


class Device(ApiResource):

    @property
    def has_switch_control(self):
        """Determine if this device has switch_control."""
        return self.type == ATTR_SWITCH

    @property
    def switch_control(self):
        if self.has_switch_control:
            return SwitchControl(self)

        return None

    def __repr__(self):
        """Object representation."""
        return "<{} - {} type({})>".format(self.id, self.title, self.type)
