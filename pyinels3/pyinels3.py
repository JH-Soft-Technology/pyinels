"""Library specified for iNels BUS CU3."""
import logging

from dataclasses import dataclass
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

    def __roomDevicesToJson(self, room_name):
        """Create json object from devices listed in preffered room."""
        d_type = None
        result = {}
        result[room_name] = {}

        devices = self.getRoomDevicesRaw(self, room_name)
        list = devices.split('\n')

        for item in list:
            start = len(item) - 1
            end = len(item)
            if start > 0:
                if item[start:end] == ":":
                    if d_type != item[0:start]:
                        d_type = item[0:start]
                        result[room_name][d_type] = []
                else:
                    dev = item.split('" ')
                    obj = {}
                    for prop in dev:
                        i = prop.split("=")
                        obj[i[0]] = i[1].replace("\"", " ").strip()
                    result[room_name][d_type].append(obj)
        return result


@dataclass
class InelsBusException(Exception):
    """Base iNels BUS exception."""
    code: str
    message: str
    trace: Exception = None


@dataclass
class InelsBusConnectionException(InelsBusException):
    """Connection exception class."""
