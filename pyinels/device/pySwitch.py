"""Inels switch class for iNels BUS."""

from pyinels.device.pyBase import pyBase


class pySwitch(pyBase):
    """Switch class based on InelsDevice."""

    async def __init__(self, device):
        """Initialize pySwitch class."""
        await super().__init__(device)
