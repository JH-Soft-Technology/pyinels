"""Const of iNels BUS."""

# Inels attributes
ATTR_DOWN = "Down"
ATTR_GROUP = "Group"
ATTR_ID = "Id"
ATTR_READ_ONLY = "Read_only"
ATTR_RELE = "Rele"
ATTR_SWITCH_OFF = "0"
ATTR_SWITCH_ON = "1"
ATTR_TEMP = "Temp"
ATTR_TEMP_SET = "Temp_set"
ATTR_TITLE = "Title"
ATTR_TYPE = "Type"
ATTR_UP = "Up"

# Internal device attributes
ATTR_SWITCH = "switch"
ATTR_LIGHT = "light"

# Device types dictionary with all determined typs translated to better
# understand
DEVICE_TYPE_DICT = {
    "undefined": "undefined",
    "lights": "light",
    "on_off": "switch",
    "shutters": "shutter",
    "heat-control": "therm",
    "heating": "heating",
    "garage": "garage"
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

NAME = "pyinels"

RANGE_BLIND = (0, 100)
RANGE_BRIGHTNESS = (0.0, 255.0)

SUPPORT_BRIGHTNESS = 1
SUPPORT_COLOR_TEMP = 4
SUPPORT_HEX_COLOR = 8
SUPPORT_RGB_COLOR = 2

VERSION = "0.4.1"
