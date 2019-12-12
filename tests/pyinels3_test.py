"""Unit testing of iNels BUS CU3 library."""
from pyinels3.pyinels3 import InelsBus3, InelsBusException
from unittest import TestCase
from unittest.mock import patch, Mock
import json

INELS_NAMESPACE = "pyinels3.pyinels3.InelsBus3"
HOST = "http://localhost"
PORT = "1000"
ROOMS = ['Basement', 'First floor', 'Front yard',
         'Back yard', 'Attic', 'Garrage']
RAW_DEVICES = """lights:
name="Main light" column="0" inels="SV_12_Garrrage" read_only="no" row="0"
name="Wall light" column="1" inels="SV_Wall_Garrage" read_only="no" row="0"
garage:
name="Doors" column="0" inels="Doors_Garaz" read_only="no" row="1"
"""


class InelsBus3Test(TestCase):
    """Class to test iNels BUS CU3 library."""

    @patch(INELS_NAMESPACE)
    def test_class_calling(self, mock_class):
        """Class instance test"""
        mock_class(HOST, PORT)

        mock_class.assert_called()
        mock_class.assert_called_once()
        mock_class.assert_called_with(HOST, PORT)

        self.assertEqual(mock_class.call_count, 1)

    @patch('xmlrpc.client.ServerProxy')
    def test_connection_failed(self, mock_proxy):
        """Test proxy connection."""
        mock_proxy.return_value = Mock()
        mock_proxy.side_effect = InelsBusException(
            'common_exception', 'Exception occur')

        with self.assertRaises(InelsBusException):
            InelsBus3(HOST, PORT).conn()

        self.assertEqual(mock_proxy.call_count, 0)

    @patch(f'{INELS_NAMESPACE}.ping')
    def test_ping_failed(self, mock_method):
        """Test ping method."""
        mock_method.return_value = False

        ret = InelsBus3(HOST, PORT).ping()

        self.assertEqual(mock_method.call_count, 1)
        self.assertFalse(ret)

    @patch(f'{INELS_NAMESPACE}.getPlcIp')
    def test_getPlcIp_success(self, mock_method):
        """Test Ip address of the PLC."""
        mock_method.return_value = "192.168.2.10"

        ret = InelsBus3(HOST, PORT).getPlcIp()

        self.assertEqual(mock_method.call_count, 1)
        self.assertEqual(ret, "192.168.2.10")

    @patch(f'{INELS_NAMESPACE}.getRooms')
    def test_getRoomsRaw_list(self, mock_method):
        """Test list of rooms defined on Connection server."""
        mock_method.return_value = ROOMS

        ret = InelsBus3(HOST, PORT).getRooms()

        self.assertEqual(mock_method.call_count, 1)
        self.assertEqual(len(ret), 6)
        self.assertEqual(ret[1], 'First floor')

    @patch(f'{INELS_NAMESPACE}.getRoomDevicesRaw')
    def test_getRoomDevices_list(self, mock_method):
        """Test list of all devices in room."""
        mock_method.return_value = RAW_DEVICES
        inels = InelsBus3(HOST, PORT)

        raw = inels.getRoomDevicesRaw('Garrage')
        self.assertEqual(mock_method.call_count, 1)
        self.assertEqual(len(raw), len(mock_method.return_value))

        json_obj = inels.getRoomDevices('Garrage')

        self.assertIsNot(type(str), type(json_obj))
        self.assertNotEqual(json_obj, raw)
        self.assertNotEqual(len(json.dumps(json_obj)), len(raw))

        self.assertEqual(json_obj['Garrage']['lights']
                         [0]['name'], 'Main light')
