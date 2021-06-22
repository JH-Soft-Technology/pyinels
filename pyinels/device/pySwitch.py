"""Inels switch class for iNels BUS."""

from pyinels.device.pyBase import pyBase


class pySwitch(pyBase):
    """Switch class based on InelsDevice."""

    def __init__(self, device):
        """Initialize pySwitch class."""
        super().__init__(device)
