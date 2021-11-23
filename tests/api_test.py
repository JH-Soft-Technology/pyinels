"""Api testing of pyInels library."""
from pyinels.api import Api

from pyinels.exception import ApiException
from tests.const_test import (
    TEST_API_CLASS_NAMESPACE,
    TEST_API_NAMESPACE,
    TEST_API_ROOM_DEVICES,
    TEST_API_READ_DATA,
    TEST_HOST,
    TEST_PORT,
    TEST_RAW_LIGHT,
    TEST_RAW_DUPLICIT_DEVICES,
    TEST_ROOMS,
    TEST_VERSION
)

from unittest.mock import patch, Mock
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

    @patch(f'{TEST_API_NAMESPACE}.resources.ApiResource.observe')
    def test_not_duplicit_entries(self, mock_method_observe):
        """Test duplicit entries inside of device list."""
        mock_method_observe.return_value = 0

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
