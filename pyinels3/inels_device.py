"""Common device class for iNels BUS."""
import logging

from dataclasses import dataclass
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


@dataclass
class InelsDevice:
    """Device class."""
    title: str
    id: str = None
    type: DeviceType = DeviceType.UNDEFINED
    temp_current: str = None
    rele: str = None
    temp_set: str = None
    down: str = None
    up: str = None
    read_only: bool = False
    value = None

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
