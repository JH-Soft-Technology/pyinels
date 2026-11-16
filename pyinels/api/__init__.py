"""Api class for iNels BUS."""
import logging
import socket
import xmlrpc.client

from functools import partial
from pyinels.device import Device

from pyinels.const import (
    ATTR_DOWN,
    ATTR_GROUP,
    ATTR_ID,
    ATTR_UNKNOWN,
    ATTR_SHUTTER,
    ATTR_TEMP,
    ATTR_THERM,
    ATTR_TITLE,
    ATTR_TYPE,
    ATTR_UP,
    ATTR_SCENE,
    DEFAULT_TIMEOUT,
    DEVICE_TYPE_DICT,
    FAULT_VARIABLE_NOT_PUBLISHED,
    INELS_BUS_ATTR_DICT
)

from pyinels.exception import (
    ApiConnectionException,
    ApiDataTypeException,
    ApiException
)


from xmlrpc.client import Fault, ServerProxy

_LOGGER = logging.getLogger(__name__)

# socket.timeout is an alias of TimeoutError since Python 3.10
TIMEOUT_ERRORS = (socket.timeout, TimeoutError)


class _TimeoutTransport(xmlrpc.client.Transport):
    """XML-RPC transport with a socket timeout."""

    def __init__(self, timeout, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._timeout = timeout

    def make_connection(self, host):
        conn = super().make_connection(host)
        conn.timeout = self._timeout
        return conn


class _TimeoutSafeTransport(xmlrpc.client.SafeTransport):
    """XML-RPC transport over https with a socket timeout."""

    def __init__(self, timeout, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._timeout = timeout

    def make_connection(self, host):
        conn = super().make_connection(host)
        conn.timeout = self._timeout
        return conn


class Api:
    """Class of iNels BUS."""

    def __init__(self, host, port, version, timeout=DEFAULT_TIMEOUT):
        """Initialize Api class."""
        self.__host = host
        self.__port = port
        self.__version = version
        self.__timeout = timeout
        self.__proxy = None
        self.__devices = None
        # variables which are not published by the Connection Server
        self.__missing_ids = set()

    @property
    def timeout(self):
        """Timeout of the calls to the Connection Server in seconds."""
        return self.__timeout

    @property
    def missing_ids(self):
        """Variables skipped because the server does not publish them."""
        return frozenset(self.__missing_ids)

    def is_missing(self, var_id):
        """True when the variable is not published by the server."""
        return var_id in self.__missing_ids

    def reset_missing(self):
        """Forget the missing variables, next fetch will try them again."""
        self.__missing_ids.clear()
        for dev in self.__devices or []:
            dev.set_levels_exported(True)

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
        if self.__devices is None:
            self.__devices = self.getAllDevices()

        return self.__devices

    def set_devices(self, devices):
        """Set device prop."""
        self.__devices = devices

    def __conn(self):
        """Instantient Api iNels BUS connection class."""
        try:
            url = self.__host + ":" + str(self.__port)
            if url.lower().startswith('https://'):
                transport = _TimeoutSafeTransport(self.__timeout)
            else:
                transport = _TimeoutTransport(self.__timeout)
            con = ServerProxy(url, transport=transport)
            return con
        except BlockingIOError as err:
            raise ApiConnectionException(err.errno, err.strerror, err)
        except Exception as err:
            raise ApiException(
                "common_exception", "Exception occur", err)

    def __call(self, method, *args):
        """Call the method of the server, timeout raises an exception."""
        try:
            return getattr(self.proxy, method)(*args)
        except TIMEOUT_ERRORS as err:
            raise ApiConnectionException(
                'timeout',
                f'Connection Server {self.__host}:{self.__port} did not '
                f'respond to {method} within {self.__timeout} s',
                err)

    def ping(self):
        """Check connection iNels BUS with ping."""
        return self.__call('ping')

    def getPlcIp(self):
        """Get Ip address of PLC."""
        return self.__call('getPlcIP')

    def getRooms(self):
        """List of all rooms from Connection server website."""
        return self.__call('getRooms')

    def getRoomDevicesRaw(self, room_name):
        """List of all devices in deffined room."""
        return self.__call('getRoomDevices', room_name)

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

        self.set_devices(devices)

        return devices

    def fetch_all_devices(self):
        """Fetch all devices data."""
        if self.__devices is not None and len(self.__devices) > 0:
            dev_ids = []

            for dev in self.__devices:
                # shutters has composed ids, and inels dont have any
                # for them so we need to use up and down identifiers instead.
                # Heat controls needs more variables (set point, levels)
                dev_ids.extend(dev.value_ids)

            data_values = self.__read_published(dev_ids)

            # rerender data on all devices
            for dev in self.__devices:
                level_ids = dev.level_ids
                if level_ids and not all(
                        dev_id in data_values for dev_id in level_ids):
                    # heat control levels are not exported, temperatures only
                    dev.set_levels_exported(False)

                value_ids = dev.value_ids
                if not all(dev_id in data_values for dev_id in value_ids):
                    # main variable is missing, device is not available
                    dev.set_value(None)
                elif len(value_ids) > 1:
                    dev.set_value({
                        f'{dev_id}': data_values[dev_id]
                        for dev_id in value_ids
                    })
                else:
                    dev.set_value({f'{dev.id}': f'{data_values[dev.id]}'})

            # return list of ids and actual data states
            return data_values

        return None

    def read(self, device_ids):
        """Get the value from the proxy by device id."""
        if not isinstance(device_ids, list):
            raise ApiDataTypeException(
                'readDeviceData', f'{device_ids} is not a list!')
        return self.__readDeviceData(device_ids)

    def __read_published(self, device_ids):
        """Read the variables, the ones not published by the server
        are skipped (and remembered, so they are not read next time)."""
        ids = [dev_id for dev_id in dict.fromkeys(device_ids)
               if dev_id not in self.__missing_ids]
        if not ids:
            return {}
        return self.__read_batch(ids)

    def __read_batch(self, ids):
        """Read the batch, failing batch is split to find missing ids."""
        try:
            return dict(self.read(ids))
        except Fault as err:
            if err.faultCode != FAULT_VARIABLE_NOT_PUBLISHED:
                raise
            if len(ids) == 1:
                self.__mark_missing(ids[0])
                return {}
            half = len(ids) // 2
            values = self.__read_batch(ids[:half])
            values.update(self.__read_batch(ids[half:]))
            return values

    def __mark_missing(self, var_id):
        """Remember the variable not published by the server."""
        if var_id not in self.__missing_ids:
            self.__missing_ids.add(var_id)
            _LOGGER.warning(
                "Variable %s is not published by the Connection Server, "
                "skipping", var_id)

    def write(self, device, value):
        """Write data to multiple devices."""
        if not hasattr(device, 'id'):
            raise ApiDataTypeException(
                'readDeviceData', f'{device} has no id')
        try:
            self.__writeValues(value)
        except ApiException:
            raise
        except Exception as err:
            raise ApiException("write_proxy", err)

    def __writeValues(self, command):
        """Write data to the proxy."""
        self.__call('writeValues', command)

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
                        .get(ATTR_TYPE)] = DEVICE_TYPE_DICT.get(
                            d_type, "unknown")

                    obj = self.__recognizeAndSetUniqueIdToDevice(obj)

                    if obj['type'] != 'unknown':

                        device = Device(obj, self)
                        device.get_value()

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

        def set_by_name(dev):
            """Set the id to the not know device from name."""
            name = dev[INELS_BUS_ATTR_DICT.get(ATTR_TITLE)].replace(" ", "_")
            dev[INELS_BUS_ATTR_DICT.get(ATTR_ID)] = name

            return dev

        # use a switch to create identifier inside of the raw data
        # from usefull attributes
        if INELS_BUS_ATTR_DICT.get(ATTR_ID) not in raw_device:
            switcher = {
                ATTR_SHUTTER: partial(set_shutter_id, raw_device),
                ATTR_THERM: partial(set_therm_id, raw_device),
                ATTR_SCENE: partial(set_by_name, raw_device),
                ATTR_UNKNOWN: partial(set_by_name, raw_device)
            }

            fnc = switcher.get(raw_device[INELS_BUS_ATTR_DICT.get(ATTR_TYPE)])
            # call selected function to set the identifier
            raw_device = fnc()

        return raw_device

    def __readDeviceData(self, device_ids):
        """Reading devices data from proxy."""
        return self.__call('read', device_ids)
