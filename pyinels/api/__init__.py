"""Api class for iNels BUS."""
import logging

from functools import partial
from pyinels.device import Device

from pyinels.const import (
    ATTR_DOWN,
    ATTR_GROUP,
    ATTR_ID,
    ATTR_SHUTTER,
    ATTR_TEMP,
    ATTR_THERM,
    ATTR_TYPE,
    ATTR_UP,
    DEVICE_TYPE_DICT,
    INELS_BUS_ATTR_DICT
)

from pyinels.exception import (
    ApiConnectionException,
    ApiDataTypeException,
    ApiException
)


from xmlrpc.client import ServerProxy

_LOGGER = logging.getLogger(__name__)


class Api:
    """Class of iNels BUS."""

    def __init__(self, host, port, version):
        """Initialize Api class."""
        self.__host = host
        self.__port = port
        self.__version = version
        self.__proxy = None
        self.__devices = None

    @property
    def proxy(self):
        """Proxy of the bus server."""
        if isinstance(self._Api__proxy, ServerProxy):
            return self.__proxy

        self.__proxy = self.__conn()
        return self.__proxy

    @property
    def devices(self):
        """Loaded devices by getAllDevices."""
        return self.__devices

    def set_devices(self, devices):
        """Set device prop."""
        self.__devices = devices

    def __conn(self):
        """Instantient Api iNels BUS connection class."""
        try:
            con = ServerProxy(self.__host + ":" + str(self.__port))
            return con
        except BlockingIOError as err:
            raise ApiConnectionException(err.errno, err.strerror, err)
        except Exception as err:
            raise ApiException(
                "common_exception", "Exception occur", err)

    def ping(self):
        """Check connection iNels BUS with ping."""
        return self.proxy.ping()

    def getPlcIp(self):
        """Get Ip address of PLC."""
        return self.proxy.getPlcIP()

    def getRooms(self):
        """List of all rooms from Connection server website."""
        return self.proxy.getRooms()

    def getRoomDevicesRaw(self, room_name):
        """List of all devices in deffined room."""
        return self.proxy.getRoomDevices(room_name)

    def getRoomDevices(self, room_name):
        """List of all devices in defined room."""
        return self.__roomDevicesToJson(room_name)

    def getAllDevices(self):
        """Get all devices from all rooms."""
        devices = []

        rooms = self.getRooms()
        # go trough all rooms
        for room in rooms:
            room_devices = self.getRoomDevices(room)
            # go trough all devices in room
            for room_dev in room_devices:
                is_in = False
                # check when duplicate devices occured
                for device in devices:
                    if device.id == room_dev.id:
                        is_in = True
                        break
                # not presented in the list, then append
                if is_in is False:
                    devices.append(room_dev)

        return devices

    def read(self, device_ids):
        """Get the value from the proxy by device id."""
        if not isinstance(device_ids, list):
            raise ApiDataTypeException(
                'readDeviceData', f'{device_ids} is not a list!')
        return self.__readDeviceData(device_ids)

    def write(self, device, value):
        """Write data to multiple devices."""
        if not hasattr(device, 'id'):
            raise ApiDataTypeException(
                'readDeviceData', f'{device} has no id')
        try:
            self.__writeValues(value)
        except Exception as err:
            raise ApiException("write_proxy", err)

    def __writeValues(self, command):
        """Write data to the proxy."""
        self.proxy.writeValues(command)

    def __roomDevicesToJson(self, room_name):
        """Create json object from devices listed in preffered room."""
        d_type = None
        devices = []

        raw_list = self.getRoomDevicesRaw(room_name)
        devices_list = raw_list.split('\n')

        for item in devices_list:
            start = len(item) - 1
            end = len(item)
            if start > 0:
                if item[start:end] == ":":
                    d_type = item[0:start]
                else:
                    json_dev = item.split('" ')
                    obj = {}
                    obj[INELS_BUS_ATTR_DICT.get(ATTR_GROUP)] = room_name

                    for prop in json_dev:
                        frag = prop.split("=")
                        obj[frag[0]] = frag[1].replace("\"", " ").strip()

                    obj[INELS_BUS_ATTR_DICT
                        .get(ATTR_TYPE)] = DEVICE_TYPE_DICT.get(d_type)

                    obj = self.__recognizeAndSetUniqueIdToDevice(obj)

                    device = Device(obj, self)
                    device.observe()

                    devices.append(device)

        return devices

    def __recognizeAndSetUniqueIdToDevice(self, raw_device):
        """Some of the devices does not have unique id
        presented in inels attribute. We need do create
        one from other unique attributes."""

        def set_shutter_id(dev):
            """Set the id to the shutter."""
            dev[INELS_BUS_ATTR_DICT.get(
                ATTR_ID)] = dev[INELS_BUS_ATTR_DICT.get(ATTR_UP)] + \
                "_" + dev[INELS_BUS_ATTR_DICT.get(ATTR_DOWN)]

            return dev

        def set_therm_id(dev):
            """Set the id to the therms."""
            dev[INELS_BUS_ATTR_DICT.get(
                ATTR_ID)] = dev[INELS_BUS_ATTR_DICT.get(ATTR_TEMP)]

            return dev

        # use a switch to create identifier inside of the raw data
        # from usefull attributes
        if INELS_BUS_ATTR_DICT.get(ATTR_ID) not in raw_device:
            switcher = {
                ATTR_SHUTTER: partial(set_shutter_id, raw_device),
                ATTR_THERM: partial(set_therm_id, raw_device)
            }

            fnc = switcher.get(raw_device[INELS_BUS_ATTR_DICT.get(ATTR_TYPE)])
            # call selected function to set the identifier
            raw_device = fnc()

        return raw_device

    def __readDeviceData(self, device_names):
        """Reading devices data from proxy."""
        return self.proxy.read(device_names)
