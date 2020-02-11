"""Common device class for iNels BUS."""
import logging

from enum import Enum

_LOGGER = logging.getLogger(__name__)


class DeviceType(Enum):
    """Enums for InelsDevice type"""
    UNDEFINED = 'undefined'
    LIGHT = 'lights'
    SWITCH = 'on_off'
    SHUTTER = 'shutters'
    THERM = 'heat-control'
    HEATING = 'heating'
    GARAGE = 'garage'

    @staticmethod
    def is_in(item):
        """Test when the item is in enum by value."""
        types = set(item.value for item in DeviceType)
        # when the item is in the enum then return enum object, otherwise
        # return object type UNDEFINED
        if item not in types:
            return DeviceType.UNDEFINED
        else:
            return DeviceType(item)


class InelsDevice:
    """Device class."""

    def __init__(self, title, id, type, proxy):
        """Initialize InelsDevice class."""
        self.title = title
        self.id = id
        self.type = type
        self.proxy = proxy
        self.temp_current: str = None
        self.rele: str = None
        self.temp_set: str = None
        self.down: str = None
        self.up: str = None
        self.read_only: bool = False
        self.value = None

    def loadFromJson(self, json_obj):
        """Load addition data from json file except id, type and title."""
        if 'therm' in json_obj:
            self.temp_current = json_obj['therm']

        if 'rele' in json_obj:
            self.rele = json_obj['rele']

        if 'stateth' in json_obj:
            self.temp_set = json_obj['stateth']

        if 'down' in json_obj:
            self.down = json_obj['down']

        if 'up' in json_obj:
            self.up = json_obj['up']

        if 'read_only' in json_obj:
            self.read_only = json_obj['read_only'] != 'no'

    def observe(self):
        """Read the current value of the device."""
        raw = self.proxy.read([self.id])
        value = raw[self.id]
        self.value = value

        return value

    def set_value(self, value):
        """Set value to the device."""
        curr_int = isinstance(self.value, int)
        new_int = isinstance(value, int)

        if (self.value != value or curr_int is not new_int):
            self.value = value
            self._write()

    def _write(self):
        """Write data to the iNels BUS unit."""
        self.proxy.write(self, self.value)
