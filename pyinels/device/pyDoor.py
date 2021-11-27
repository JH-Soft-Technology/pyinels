"""Inels door class for iNels BUS."""
from time import sleep
from pyinels.device.pyBase import pyBase

from pyinels.const import (
    ATTR_SWITCH_ON,
    ATTR_SWITCH_OFF
)

#############################################################################
# Note!
# This class is specific. turn_off and turn_on do the same job and the state
# and the update method does not have a sense with this device
##############################################################################


class pyDoor(pyBase):
    """Inels class based on InelsDevice."""

    def __init__(self, device):
        """Initialize pyDoor class."""
        super().__init__(device)

    def turn_off(self):
        """Trigger impoulse button. Write 1 to device and then 0 back."""
        self._device.write_value(ATTR_SWITCH_ON)
        sleep(2)  # delay to be sure that the pulse was sent
        self._device.write_value(ATTR_SWITCH_OFF)

    def turn_on(self):
        """Same as turn off."""
        self.turn_off()

    def update(self):
        """Does not have any sens due to the pulse behavior."""
        return 0

    @property
    def state(self):
        """This property does not have any sense due to the pulse behavior."""
        return False
