"""Api testing of pyInels library."""
import socket

from xmlrpc.client import Fault

from pyinels.api import Api, _TimeoutSafeTransport, _TimeoutTransport
from pyinels.const import DEFAULT_TIMEOUT, HEAT_LEVEL_ATTENUATION
from pyinels.device.pyShutter import pyShutter
from pyinels.device.pyTherm import pyTherm

from pyinels.exception import ApiConnectionException, ApiException
from tests.const_test import (
    TEST_API_CLASS_NAMESPACE,
    TEST_API_NAMESPACE,
    TEST_API_ROOM_DEVICES,
    TEST_API_READ_DATA,
    TEST_HOST,
    TEST_PORT,
    TEST_RAW_LIGHT,
    TEST_RAW_DUPLICIT_DEVICES,
    TEST_RETURN_RESOURCE_SHUTTER_UP,
    TEST_ROOMS,
    TEST_VERSION,
    TEST_RAW_SHUTTER,
    TEST_RAW_SCENE
)

from unittest.mock import patch, Mock, PropertyMock
from unittest import TestCase

LIGHT_ID = 'SV_12_Garage'
LIGHT_NAME = 'Main light'

LIGHT_RETURN_OFF = {LIGHT_ID: 0}
LIGHT_RETURN_ON = {LIGHT_ID: 1}


class ApiTest(TestCase):
    """Class to test pyInels api library."""

    def setUp(self):
        """Setup all necessary instances nad mocks."""
        self.patches = [
            patch(f'{TEST_API_CLASS_NAMESPACE}.ping', return_value=True),
        ]

        self.api = Api(TEST_HOST, TEST_PORT, TEST_VERSION)

        # patching ping method in IneslBus3. It will be executed every test
        for p in self.patches:
            p.start()

    def tearDown(self):
        """Destroy all instances and mocks."""
        self.api = None
        patch.stopall()
        self.patches = None

    @patch(TEST_API_CLASS_NAMESPACE)
    def test_class_calling(self, mock_class):
        """Class instance test."""
        mock_class(TEST_HOST, TEST_PORT, TEST_VERSION)

        mock_class.assert_called()
        mock_class.assert_called_once()
        mock_class.assert_called_with(TEST_HOST, TEST_PORT, TEST_VERSION)

        self.assertEqual(mock_class.call_count, 1)

    @patch('xmlrpc.client.ServerProxy')
    def test_connection_failed(self, mock_server):
        """Test api connection."""
        mock_server.return_value = Mock()
        mock_server.side_effect = ApiException(
            'common_exception', 'Exception occur')

        ret = self.api.ping()
        self.assertEqual(True, ret)
        self.assertEqual(mock_server.call_count, 0)

    @patch(f'{TEST_API_CLASS_NAMESPACE}.ping')
    def test_ping_failed(self, mock_method):
        """Test ping method."""
        mock_method.return_value = False
        ret = self.api.ping()

        self.assertEqual(mock_method.call_count, 1)
        self.assertFalse(ret)

    @patch(f'{TEST_API_CLASS_NAMESPACE}.getPlcIp')
    def test_getPlcIp_success(self, mock_method):
        """Test Ip address of the PLC."""
        RET_VAL = "192.168.2.10"

        mock_method.return_value = RET_VAL
        ret = self.api.getPlcIp()

        self.assertEqual(mock_method.call_count, 1)
        self.assertEqual(ret, RET_VAL)

    @patch(f'{TEST_API_CLASS_NAMESPACE}.getRooms')
    def test_getRoomsRaw_list(self, mock_method):
        """Test list of rooms defined on Connection server."""
        mock_method.return_value = TEST_ROOMS

        ret = self.api.getRooms()

        self.assertEqual(mock_method.call_count, 1)
        self.assertEqual(len(ret), 6)
        self.assertEqual(ret[1], 'First floor')

    @patch(f'{TEST_API_CLASS_NAMESPACE}.{TEST_API_ROOM_DEVICES}')
    def test_getRoomDevices_list(self, mock_method):
        """Test list of all devices in room."""
        mock_method.return_value = TEST_RAW_LIGHT
        raw = self.api.getRoomDevicesRaw('room')

        self.assertEqual(mock_method.call_count, 1)
        self.assertEqual(len(raw), len(mock_method.return_value))

        # this is the way how to mock private method
        with patch.object(
            self.api,
            TEST_API_READ_DATA,
            return_value=LIGHT_RETURN_OFF
        ):
            with patch.object(self.api, 'ping', return_value=True):
                obj_list = self.api.getRoomDevices('room')

                device = obj_list[0]

                self.assertGreater(len(obj_list), 0)
                self.assertEqual(device.id, LIGHT_ID)
                self.assertEqual(device.title, LIGHT_NAME)

                patch.stopall()
                device_value = self.api.read([device.id])
                self.assertEqual(device_value, LIGHT_RETURN_OFF)

    @patch(f'{TEST_API_NAMESPACE}.resources.ApiResource.get_value')
    def test_not_duplicit_entries(self, mock_method_get_value):
        """Test duplicit entries inside of device list."""
        mock_method_get_value.return_value = 0

        with patch.object(self.api, 'ping', return_value=True):
            with patch.object(self.api, TEST_API_ROOM_DEVICES,
                              return_value=TEST_RAW_DUPLICIT_DEVICES):
                obj_list = self.api.getRoomDevices('room')

                with patch.object(self.api, "getRooms", return_value=["room"]):

                    with patch.object(self.api, "getRoomDevices",
                                      return_value=obj_list):
                        devices = self.api.getAllDevices()

                        self.assertEqual(len(devices), 48)
                        self.assertGreater(len(obj_list), len(devices))

    @patch(f'{TEST_API_NAMESPACE}.resources.ApiResource.get_value')
    def test_fetch_all_data_sutters(self, mocked):
        """Testing all data fetch from inels."""
        mocked.return_value = TEST_RETURN_RESOURCE_SHUTTER_UP

        with patch.object(self.api, 'ping', return_value=True):
            with patch.object(self.api, TEST_API_ROOM_DEVICES,
                              return_value=TEST_RAW_SHUTTER):
                obj_list = self.api.getRoomDevices('room')

                with patch.object(self.api, "getRooms",
                                  return_value=["room"]):
                    with patch.object(self.api, "getRoomDevices",
                                      return_value=obj_list):
                        devices = self.api.getAllDevices()

                        with patch.object(self.api, "read",
                                          return_value=mocked.return_value):
                            shutt = pyShutter(devices[0])

                            with patch.object(self.api, "write",
                                              return_value=None):
                                shutt.pull_up()

                                fetch = self.api.fetch_all_devices()
                                self.assertEqual(shutt.value, fetch)

    @patch(f'{TEST_API_NAMESPACE}.resources.ApiResource.get_value')
    def test_create_unknown_device(self, mocked):
        """Testing not known device were created by API."""
        mocked.return_value = TEST_RETURN_RESOURCE_SHUTTER_UP

        with patch.object(self.api, 'ping', return_value=True):
            with patch.object(self.api, TEST_API_ROOM_DEVICES,
                              return_value=TEST_RAW_SCENE):
                obj_list = self.api.getRoomDevices('room')

                with patch.object(self.api, "getRooms", return_value=["room"]):

                    with patch.object(self.api, "getRoomDevices",
                                      return_value=obj_list):
                        devices = self.api.getAllDevices()

                        self.assertEqual(1, len(devices))


RAW_RESILIENCE_DEVICES = """lights:
name="A" column="0" inels="SV_A" read_only="no" row="0"
name="B" column="1" inels="SV_B" read_only="no" row="0"
name="C" column="2" inels="SV_C" read_only="no" row="0"
heat-control:
name="Pokoj" read_only="no" therm="Pokoj_dole_Temperature" column="1" \
stateth="Pokoj_dole_StateTH" rele="D" row="4"
"""

RESILIENCE_VALUES = {
    "SV_A": 1,
    "SV_B": 0,
    "SV_C": 1,
    "Pokoj_dole_Temperature": 22.75,
    "Pokoj_dole_StateTH": 21.0,
    "Pokoj_dole_StateM": 0,
    "Pokoj_dole_StateU": 1,
    "Pokoj_dole_StateN": 0,
    "Pokoj_dole_StateK": 0,
}

THERM_LEVEL_IDS = ["Pokoj_dole_StateM", "Pokoj_dole_StateU",
                   "Pokoj_dole_StateN", "Pokoj_dole_StateK"]


class FakeServer:
    """Connection Server reading only the published variables."""

    def __init__(self, values):
        self.values = dict(values)
        self.calls = []

    def unpublish(self, *var_ids):
        for var_id in var_ids:
            self.values.pop(var_id, None)

    def read(self, ids):
        self.calls.append(list(ids))
        if any(var_id not in self.values for var_id in ids):
            raise Fault(8002, 'Variable does not exist')
        return {var_id: self.values[var_id] for var_id in ids}


class ApiTimeoutTest(TestCase):
    """Timeout of the calls to the Connection Server."""

    def test_default_timeout(self):
        """Default timeout is used by the transport."""
        api = Api(TEST_HOST, TEST_PORT, TEST_VERSION)
        transport = api.proxy._ServerProxy__transport

        self.assertEqual(api.timeout, DEFAULT_TIMEOUT)
        self.assertIsInstance(transport, _TimeoutTransport)
        self.assertEqual(transport._timeout, DEFAULT_TIMEOUT)

    def test_custom_timeout(self):
        """Timeout given to the Api is passed to the transport."""
        api = Api(TEST_HOST, TEST_PORT, TEST_VERSION, timeout=5)
        transport = api.proxy._ServerProxy__transport

        self.assertEqual(api.timeout, 5)
        self.assertEqual(transport._timeout, 5)

    def test_https_timeout(self):
        """Https url uses the safe transport with the timeout."""
        api = Api("https://localhost", TEST_PORT, TEST_VERSION, timeout=5)
        transport = api.proxy._ServerProxy__transport

        self.assertIsInstance(transport, _TimeoutSafeTransport)
        self.assertEqual(transport._timeout, 5)

    def test_connection_has_timeout(self):
        """Connection created by the transport has the timeout."""
        conn = _TimeoutTransport(3).make_connection("localhost:1000")
        self.assertEqual(conn.timeout, 3)

        conn = _TimeoutSafeTransport(4).make_connection("localhost:1000")
        self.assertEqual(conn.timeout, 4)

    def test_read_timeout(self):
        """Timeout of the read raises the connection exception."""
        api = Api(TEST_HOST, TEST_PORT, TEST_VERSION, timeout=1)
        proxy = Mock()
        proxy.read.side_effect = socket.timeout('timed out')

        with patch(f'{TEST_API_CLASS_NAMESPACE}.proxy',
                   new_callable=PropertyMock, return_value=proxy):
            with self.assertRaises(ApiConnectionException) as ctx:
                api.read(['SV_A'])

        self.assertEqual(ctx.exception.code, 'timeout')

    def test_ping_timeout(self):
        """Timeout of the ping raises the connection exception."""
        api = Api(TEST_HOST, TEST_PORT, TEST_VERSION, timeout=1)
        proxy = Mock()
        proxy.ping.side_effect = TimeoutError('timed out')

        with patch(f'{TEST_API_CLASS_NAMESPACE}.proxy',
                   new_callable=PropertyMock, return_value=proxy):
            with self.assertRaises(ApiConnectionException):
                api.ping()


class ApiMissingVariableTest(TestCase):
    """Variables not published by the Connection Server."""

    def setUp(self):
        """Load the devices from the fake server."""
        self.server = FakeServer(RESILIENCE_VALUES)
        self.patches = [
            patch(f'{TEST_API_CLASS_NAMESPACE}.getRooms',
                  return_value=['Room']),
            patch(f'{TEST_API_CLASS_NAMESPACE}.{TEST_API_ROOM_DEVICES}',
                  return_value=RAW_RESILIENCE_DEVICES),
            patch(f'{TEST_API_CLASS_NAMESPACE}.{TEST_API_READ_DATA}',
                  side_effect=self.server.read),
        ]
        for p in self.patches:
            p.start()

        self.api = Api(TEST_HOST, TEST_PORT, TEST_VERSION)
        self.devices = {dev.id: dev for dev in self.api.getAllDevices()}

    def tearDown(self):
        """Stop the mocks."""
        patch.stopall()

    def test_missing_variable_is_skipped(self):
        """Other devices get values, the missing one is unavailable."""
        self.server.unpublish("SV_B")

        with self.assertLogs('pyinels.api', level='WARNING') as logs:
            self.api.fetch_all_devices()
            self.server.calls.clear()
            self.api.fetch_all_devices()

        warnings = [r for r in logs.output if 'SV_B' in r]
        self.assertEqual(len(warnings), 1)
        self.assertEqual(self.api.missing_ids, frozenset({"SV_B"}))

        # second fetch does not ask for the missing variable
        self.assertEqual(len(self.server.calls), 1)
        self.assertNotIn("SV_B", self.server.calls[0])

        self.assertEqual(self.devices["SV_A"].value, {"SV_A": "1"})
        self.assertEqual(self.devices["SV_C"].value, {"SV_C": "1"})
        self.assertIsNone(self.devices["SV_B"].value)

        therm = pyTherm(self.devices["Pokoj_dole_Temperature"])
        self.assertEqual(therm.current_temperature, 22.75)
        self.assertEqual(therm.level, HEAT_LEVEL_ATTENUATION)

        # unavailable without asking the server again
        self.server.calls.clear()
        self.assertFalse(self.devices["SV_B"].is_available)
        self.assertEqual(self.server.calls, [])

    def test_reset_missing(self):
        """After reset the missing variable is read again."""
        self.server.unpublish("SV_B")
        with self.assertLogs('pyinels.api', level='WARNING'):
            self.api.fetch_all_devices()

        self.server.values["SV_B"] = 1
        self.api.reset_missing()
        self.api.fetch_all_devices()

        self.assertEqual(self.api.missing_ids, frozenset())
        self.assertEqual(self.devices["SV_B"].value, {"SV_B": "1"})

    def test_missing_levels_keep_temperatures(self):
        """Heat control without exported levels has temperatures."""
        self.server.unpublish(*THERM_LEVEL_IDS)

        with self.assertLogs('pyinels.api', level='WARNING'):
            self.api.fetch_all_devices()

        device = self.devices["Pokoj_dole_Temperature"]
        therm = pyTherm(device)

        self.assertEqual(device.level_ids, [])
        self.assertEqual(therm.current_temperature, 22.75)
        self.assertEqual(therm.target_temperature, 21.0)
        self.assertEqual(therm.levels, [])
        self.assertTrue(device.is_available)

    def test_missing_variable_at_setup(self):
        """Device with missing variable does not break the loading."""
        self.server.unpublish("SV_C")

        devices = {dev.id: dev for dev in self.api.getAllDevices()}

        self.assertEqual(len(devices), 4)
        self.assertIsNone(devices["SV_C"].value)
        self.assertEqual(devices["SV_A"].value, {"SV_A": 1})

    def test_other_fault_is_raised(self):
        """Other faults than missing variable are not swallowed."""
        with patch(f'{TEST_API_CLASS_NAMESPACE}.{TEST_API_READ_DATA}',
                   side_effect=Fault(1, 'Server error')):
            with self.assertRaises(Fault):
                self.api.fetch_all_devices()
