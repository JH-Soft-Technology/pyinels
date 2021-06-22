"""Common device class for iNels BUS."""
from pyinels.api.resources import ApiResource


class Device(ApiResource):
    """Device class."""

    def __init__(self, entity, api):
        """Initialize device class."""
        super().__init__(entity, api)

    def __repr__(self):
        """Object representation."""
        return "<{} - {} type({})>".format(self.id, self.title, self.type)
