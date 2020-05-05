"""Common device class for iNels BUS."""
from pyinels.api.resources import ApiResource


class Device(ApiResource):
    def __repr__(self):
        """Object representation."""
        return "<{} - {} type({})>".format(self.id, self.title, self.type)
