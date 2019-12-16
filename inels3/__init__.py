"""Library specified for iNels BUS CU3."""
import logging

from dataclasses import dataclass
from inels3.device import DeviceType, InelsDevice
from xmlrpc.client import ServerProxy

_LOGGER = logging.getLogger(__name__)


@dataclass
class InelsBus3:
    """Class for iNels BUS CU3 version."""
    __host: str
    __port: str
    __proxy = None

    def conn(self):
        """Instantient InelsBus3 class."""
        try:
            if self.__proxy is None:
                self.__proxy = ServerProxy(
                    self.__host + ":" + str(self.__port))
                self.__proxy.ping()
            return self.__proxy
        except BlockingIOError as err:
            raise InelsBusConnectionException(err.errno, err.strerror, err)
        except Exception as err:
            raise InelsBusException(
                "common_exception", "Exception occur", err)

    def ping(self):
        """Check connection iNels BUS with ping."""
        return self.conn().ping()

    def getPlcIp(self):
        """Get Ip address of PLC."""
        return self.conn().getPlcIP()

    def getRooms(self):
        """List of all rooms from Connection server website."""
        return self.conn().getRooms()

    def getRoomDevicesRaw(self, room_name):
        """List of all devices in deffined room."""
        return self.conn().getRoomDevices(room_name)

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

    def observe(self, device_ids):
        """Get the value from the proxy by device id."""
        if not isinstance(device_ids, list):
            raise InelsBusDataTypeException(
                'readDeviceData', f'{device_ids} is not a list!')
        return self.__readDeviceData(device_ids)

    def write(self, device):
        """Write data to multiple devices."""
        if not isinstance(device, InelsDevice):
            raise InelsBusDataTypeException(
                'readDeviceData', f'{device} is not object InelsDevice')
        try:
            self.__writeValues(device.value)
        except Exception as err:
            raise InelsBusException("write_proxy", err)

    def __writeValues(self, command):
        """Write data to the proxy."""
        self.conn().writeValues(command)

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
                    for prop in json_dev:
                        frag = prop.split("=")
                        obj[frag[0]] = frag[1].replace("\"", " ").strip()

                    device = self.__loadDevice(obj, d_type)
                    devices.append(device)

        return devices

    def __readDeviceData(self, device_names):
        """Reading devices data from proxy."""
        return self.conn().read(device_names)

    def __loadDevice(self, json_device, d_type: str):
        """Load device to the object structure"""
        id = None
        if 'inels' in json_device:
            id = json_device['inels']

        device = InelsDevice(
            json_device['name'],
            id,
            DeviceType.is_in(d_type))
        # load data from json
        device.loadFromJson(json_device)

        # read value state of that device
        device.value = self.__readDeviceData(
            self.__get_val_name(device, device.type))

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
