"""Api class for iNels BUS."""

import logging

from pyinels.device import Device

from pyinels.const import DEVICE_TYPE_DICT

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

    @property
    def proxy(self):
        """Proxy of the bus server."""
        if isinstance(self._Api__proxy, ServerProxy):
            return self.__proxy

        self.__proxy = self.__conn()
        self.ping()
        return self.__proxy

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
        rooms = self.getRooms()

        devices = []
        for room in rooms:
            devices += self.getRoomDevices(room)

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
            obj = {}
            obj[device.id] = value

            self.__writeValues(obj)
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
        list = raw_list.split('\n')

        for item in list:
            start = len(item) - 1
            end = len(item)
            if start > 0:
                if item[start:end] == ":":
                    d_type = item[0:start]
                else:
                    json_dev = item.split('" ')
                    obj = {}
                    obj["group"] = room_name

                    for prop in json_dev:
                        frag = prop.split("=")
                        obj[frag[0]] = frag[1].replace("\"", " ").strip()

                    obj["type"] = DEVICE_TYPE_DICT.get(d_type)
                    devices.append(Device(obj, self))
        return devices

    def __readDeviceData(self, device_names):
        """Reading devices data from proxy."""
        return self.proxy.read(device_names)
