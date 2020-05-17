"""Common device class for iNels BUS."""
from pyinels.api.resources import ApiResource

from pyinels.const import (
    ATTR_LIGHT_DIMMABLE,
    ATTR_LIGHT
)


class Device(ApiResource):
    """Device class."""

    def __init__(self, entity, api):
        """Initialize device class."""
        super().__init__(entity, api)

        if self.type == ATTR_LIGHT:
            if self.is_available is True:
                if isinstance(self.value, float) is True:
                    self.type = ATTR_LIGHT_DIMMABLE

    def __repr__(self):
        """Object representation."""
        return "<{} - {} type({})>".format(self.id, self.title, self.type)
