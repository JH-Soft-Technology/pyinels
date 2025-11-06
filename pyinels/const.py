"""Const of iNels BUS."""

# Inels attributes
ATTR_ADDITION = "Koef_add"
ATTR_DECIMAL_DIGITS = "Decimal_digits"
ATTR_DOWN = "Down"
ATTR_GROUP = "Group"
ATTR_ID = "Id"
ATTR_MAX_DISP = "Max_disp"
ATTR_MIN_DISP = "Min_disp"
ATTR_MULTIPLICATOR = "Koef_mult"
ATTR_READ_ONLY = "Read_only"
ATTR_RELE = "Rele"
ATTR_STOP = "Stop"
ATTR_SWITCH_OFF = 0
ATTR_SWITCH_ON = 1
ATTR_TEMP = "Temp"
ATTR_TEMP_SET = "Temp_set"
ATTR_TITLE = "Title"
ATTR_TYPE = "Type"
ATTR_UNITS = "Units"
ATTR_UP = "Up"


# Internal device attributes
ATTR_AIRING = "airing"
ATTR_DOOR = "door"
ATTR_HEATING = "heating"
ATTR_LIGHT = "light"
ATTR_METER = "meter"
ATTR_SCENE = "scenes"
ATTR_SHUTTER = "shutter"
ATTR_SWITCH = "switch"
ATTR_THERM = "therm"
ATTR_UNKNOWN = "unknown"

# Device types dictionary with all determined typs translated to better
# understand
DEVICE_TYPE_DICT = {
    "airing": "airing",
    "garage": "door",
    "gate": "door",
    "hc4": "unknown",
    "heating": "heating",
    "heat-control": "therm",
    "lights": "light",
    "meter": "meter",
    "on_off": "switch",
    "scenes": "scenes",
    "shutters": "shutter",
    "thermals": "thermals",
    "undefined": "undefined",
}

DIRECTIONS_DICT = {
    "Down": "down",
    "Stop": "stop",
    "Up": "up",
}

INELS_BUS_ATTR_DICT = {
    "Decimal_digits": "decimal_digits",
    "Down": "down",
    "Group": "group",
    "Id": "inels",
    "Koef_add": "koef_add",
    "Koef_mult": "koef_mult",
    "Max_disp": "max_disp",
    "Min_disp": "min_disp",
    "Read_only": "read_only",
    "Rele": "rele",
    "Temp": "therm",
    "Temp_set": "stateth",
    "Title": "name",
    "Type": "type",
    "Units": "units",
    "Up": "up"
}

UNITS_DICT = {
    "stu": "Degree",
    "%": "Percentage"
}

ERROR_VALUE = -1

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

STATE_CLOSED = "closed"
STATE_CLOSING = "closing"
STATE_OPEN = "open"
STATE_OPENING = "opening"

VERSION = "0.6.16"
