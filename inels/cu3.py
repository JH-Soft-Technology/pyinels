"""Library specified for iNels BUS CU3."""
import logging

from dataclasses import dataclass
from inels.device import DeviceType, InelsDevice
from xmlrpc.client import ServerProxy

_LOGGER = logging.getLogger(__name__)


class InelsBus3:
    """Class for iNels BUS CU3 version."""

    def __init__(self, host, port):
        """Initialize InelsBus3 class."""
        self.__host = host
        self.__port = port
        self.__proxy = None

    @property
    def proxy(self):
        """Proxy of the cu3 server."""
        if isinstance(self._InelsBus3__proxy, ServerProxy):
            return self.__proxy

        self.__proxy = self.__conn()
        self.ping()
        return self.__proxy

    def __conn(self):
        """Instantient InelsBus3 class."""
        try:
            con = ServerProxy(self.__host + ":" + str(self.__port))
            return con
        except BlockingIOError as err:
            raise InelsBusConnectionException(err.errno, err.strerror, err)
        except Exception as err:
            raise InelsBusException(
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
            raise InelsBusDataTypeException(
                'readDeviceData', f'{device_ids} is not a list!')
        return self.__readDeviceData(device_ids)

    def write(self, device, value):
        """Write data to multiple devices."""
        if not isinstance(device, InelsDevice):
            raise InelsBusDataTypeException(
                'readDeviceData', f'{device} is not object InelsDevice')
        try:
            obj = {}
            obj[device.id] = value

            self.__writeValues(obj)
        except Exception as err:
            raise InelsBusException("write_proxy", err)

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

                    device = self.__loadDevice(obj, d_type)
                    devices.append(device)

        return devices

    def __readDeviceData(self, device_names):
        """Reading devices data from proxy."""
        return self.proxy.read(device_names)

    def __loadDevice(self, json_device, d_type: str):
        """Load device to the object structure"""
        id = None
        if 'inels' in json_device:
            id = json_device['inels']

        device = InelsDevice(
            json_device['name'],
            id,
            DeviceType.is_in(d_type),
            self.proxy)
        # load data from json
        device.loadFromJson(json_device)

        return device

    @staticmethod
    def __get_val_name(device: InelsDevice, d_type: DeviceType):
        """SHUTTER is quite specific object. It does not have ID.
        UP and DOWN is only defined, which each means ID.
        I need to get a list of device.id to send them to the proxy method
        read. When SHUTTER comes, than I need to make a
        list of up and down props. And send them together to the proxy."""
        return {
            DeviceType.SHUTTER: [device.up, device.down],
            DeviceType.THERM: [device.temp_current, device.temp_set]
        }.get(d_type, [device.id])


@dataclass
class InelsBusException(Exception):
    """Base iNels BUS exception."""
    code: str
    message: str
    trace: Exception = None


@dataclass
class InelsBusConnectionException(InelsBusException):
    """Connection exception class."""


@dataclass
class InelsBusDataTypeException(InelsBusException):
    """Bad type exception."""
