"""Const of iNels BUS."""

# Inels attributes
ATTR_DOWN = "Down"
ATTR_GROUP = "Group"
ATTR_ID = "Id"
ATTR_READ_ONLY = "Read_only"
ATTR_RELE = "Rele"
ATTR_SWITCH_OFF = 0
ATTR_SWITCH_ON = 1
ATTR_TEMP = "Temp"
ATTR_TEMP_SET = "Temp_set"
ATTR_TITLE = "Title"
ATTR_TYPE = "Type"
ATTR_UP = "Up"
ATTR_STOP = "Stop"

# Internal device attributes
ATTR_SWITCH = "switch"
ATTR_LIGHT = "light"
ATTR_DOOR = "door"
ATTR_SHUTTER = "shutter"
ATTR_HEATING = "heating"
ATTR_THERM = "therm"

# Device types dictionary with all determined typs translated to better
# understand
DEVICE_TYPE_DICT = {
    "undefined": "undefined",
    "lights": "light",
    "on_off": "switch",
    "shutters": "shutter",
    "heat-control": "therm",
    "heating": "heating",
    "garage": "door",
    "gate": "door"
}

INELS_BUS_ATTR_DICT = {
    "Id": "inels",
    "Title": "name",
    "Type": "type",
    "Temp": "therm",
    "Rele": "rele",
    "Temp_set": "stateth",
    "Down": "down",
    "Up": "up",
    "Read_only": "read_only",
    "Group": "group"
}

DIRECTIONS_DICT = {
    "Up": "up",
    "Dwon": "down",
    "Stop": "stop"
}

NAME = "pyinels"

RANGE_BLIND = (0, 100)
RANGE_BRIGHTNESS = (0.0, 100.0)

SUPPORT_BRIGHTNESS = 1
SUPPORT_RGB_COLOR = 2
SUPPORT_COLOR_TEMP = 4
SUPPORT_HEX_COLOR = 8

# supported features
SUPPORT_OPEN = 1
SUPPORT_CLOSE = 2
SUPPORT_SET_POSITION = 4,
SUPPORT_STOP = 8
SUPPORT_OPEN_TILT = 16
SUPPORT_CLOSE_TILT = 32
SUPPORT_STOP_TILT = 64

STATE_OPEN = "open"
STATE_OPENING = "opening"
STATE_CLOSED = "closed"
STATE_CLOSING = "closing"

VERSION = "0.6.3"
