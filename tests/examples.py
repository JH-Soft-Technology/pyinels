"""Usaage examples."""
from inels.cu3 import InelsBus3

# fill the IP address and Port of your iNels PLC
inels = InelsBus3('http://localhost', '9000')

# checking when the connection is established successfuly
available = inels.ping()

# get the list of all rooms from Connection server
rooms = inels.getRooms()

# get all devices from current room. Room can be taken from rooms property
roomDevices = inels.getRoomDevices('room name')

# get the raw data from the PLC formated in string. Each device is on
# separated line it's just used for developing and data checking purposes
raw = inels.getRoomDevicesRaw('room name')

# get all devices from all rooms in one list. List contains
# object InelsDevice. This is the most used method.
devices = inels.getAllDevices()

# get the value / state of the device. Some special devices like SHUTTERS or
# THERM does not have id. You need to use up/down/temp_current/temp_set as
# param. Method is used for getting the state. So this method will be
# the most offen called one
data = inels.observe('InelsDevice.id')

# Write state/data to the PLC.
# You need to change the value of the object device to what ever you want
inels.write('device')
