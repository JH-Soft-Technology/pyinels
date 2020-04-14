"""Api testing of pyInels library."""
from pyinels.api import Api

from pyinels.exception import ApiException
from tests.const_test import (
    TEST_API_CLASS_NAMESPACE,
    TEST_DATA_SWITCH,
    TEST_HOST,
    TEST_PORT,
    TEST_RAW_DEVICES,
    TEST_ROOMS,
    TEST_VERSION
)

from unittest.mock import patch, Mock
from unittest import TestCase


class ApiTest(TestCase):
    """Class to test pyInels api library."""

    def setUp(self):
        """Setup all necessary instances nad mocks."""
        self.patches = [
            patch(f'{TEST_API_CLASS_NAMESPACE}.ping', return_value=True),
            patch(f'{TEST_API_CLASS_NAMESPACE}.read',
                  return_value={TEST_DATA_SWITCH['id']: 1}),
        ]

        self.proxy = Api(TEST_HOST, TEST_PORT, TEST_VERSION)

        # patching ping method in IneslBus3. It will be executed every test
        for p in self.patches:
            p.start()

    def tearDown(self):
        """Destroy all instances and mocks."""
        self.proxy = None
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
        """Test proxy connection."""
        mock_server.return_value = Mock()
        mock_server.side_effect = ApiException(
            'common_exception', 'Exception occur')

        ret = self.proxy.ping()
        self.assertEqual(True, ret)
        self.assertEqual(mock_server.call_count, 0)

    @patch(f'{TEST_API_CLASS_NAMESPACE}.ping')
    def test_ping_failed(self, mock_method):
        """Test ping method."""
        mock_method.return_value = False
        ret = self.proxy.ping()

        self.assertEqual(mock_method.call_count, 1)
        self.assertFalse(ret)

    @patch(f'{TEST_API_CLASS_NAMESPACE}.getPlcIp')
    def test_getPlcIp_success(self, mock_method):
        """Test Ip address of the PLC."""
        mock_method.return_value = "192.168.2.10"

        ret = self.proxy.getPlcIp()

        self.assertEqual(mock_method.call_count, 1)
        self.assertEqual(ret, "192.168.2.10")

    @patch(f'{TEST_API_CLASS_NAMESPACE}.getRooms')
    def test_getRoomsRaw_list(self, mock_method):
        """Test list of rooms defined on Connection server."""
        mock_method.return_value = TEST_ROOMS

        ret = self.proxy.getRooms()

        self.assertEqual(mock_method.call_count, 1)
        self.assertEqual(len(ret), 6)
        self.assertEqual(ret[1], 'First floor')

    @patch(f'{TEST_API_CLASS_NAMESPACE}.getRoomDevicesRaw')
    def test_getRoomDevices_list(self, mock_method):
        """Test list of all devices in room."""
        mock_method.return_value = TEST_RAW_DEVICES
        raw = self.proxy.getRoomDevicesRaw('room')

        self.assertEqual(mock_method.call_count, 1)
        self.assertEqual(len(raw), len(mock_method.return_value))

        # this is the way how to mock private method
        with patch.object(
            self.proxy,
            '_Api__readDeviceData',
            return_value={'Doors_Garage': 0}
        ):
            with patch.object(self.proxy, 'ping', return_value=True):
                obj_list = self.proxy.getRoomDevices('room')

                device = obj_list[0]

                self.assertGreater(len(obj_list), 0)
                self.assertEqual(device.id, 'Doors_Garage')
                self.assertEqual(device.title, 'Doors')

                patch.stopall()
                device_value = self.proxy.read([device.id])
                self.assertEqual(device_value, {'Doors_Garage': 0})
