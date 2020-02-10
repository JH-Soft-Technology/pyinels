"""Unit testing of iNels BUS CU3 library."""

from tests.const_test import (
    TEST_HOST,
    TEST_INELS_BUS3_NAMESPACE,
    TEST_PORT,
    TEST_RAW_DEVICES,
    TEST_ROOMS,
    TEST_DATA_GARAGE,
    TEST_DATA_HEATING,
    TEST_DATA_LIGHT,
    TEST_DATA_SHUTTER,
    TEST_DATA_SWITCH,
    TEST_DATA_THERM
)
from inels.cu3 import (
    InelsBus3,
    InelsBusException,
    InelsBusDataTypeException
)
from inels.device import DeviceType, InelsDevice
from unittest.mock import patch, Mock
from unittest import TestCase


class InelsBus3Test(TestCase):
    """Class to test iNels BUS CU3 library."""

    @patch(TEST_INELS_BUS3_NAMESPACE)
    def test_class_calling(self, mock_class):
        """Class instance test."""
        mock_class(TEST_HOST, TEST_PORT)

        mock_class.assert_called()
        mock_class.assert_called_once()
        mock_class.assert_called_with(TEST_HOST, TEST_PORT)

        self.assertEqual(mock_class.call_count, 1)

    @patch('xmlrpc.client.ServerProxy')
    def test_connection_failed(self, mock_server):
        """Test proxy connection."""
        mock_server.return_value = Mock()
        mock_server.side_effect = InelsBusException(
            'common_exception', 'Exception occur')

        inels = InelsBus3(TEST_HOST, TEST_PORT)

        with patch.object(inels, 'ping', return_value=True):
            ret = inels.ping()
            self.assertEqual(True, ret)

        self.assertEqual(mock_server.call_count, 0)

    @patch(f'{TEST_INELS_BUS3_NAMESPACE}.ping')
    def test_ping_failed(self, mock_method):
        """Test ping method."""
        mock_method.return_value = False

        ret = InelsBus3(TEST_HOST, TEST_PORT).ping()

        self.assertEqual(mock_method.call_count, 1)
        self.assertFalse(ret)

    @patch(f'{TEST_INELS_BUS3_NAMESPACE}.getPlcIp')
    def test_getPlcIp_success(self, mock_method):
        """Test Ip address of the PLC."""
        mock_method.return_value = "192.168.2.10"

        ret = InelsBus3(TEST_HOST, TEST_PORT).getPlcIp()

        self.assertEqual(mock_method.call_count, 1)
        self.assertEqual(ret, "192.168.2.10")

    @patch(f'{TEST_INELS_BUS3_NAMESPACE}.getRooms')
    def test_getRoomsRaw_list(self, mock_method):
        """Test list of rooms defined on Connection server."""
        mock_method.return_value = TEST_ROOMS

        ret = InelsBus3(TEST_HOST, TEST_PORT).getRooms()

        self.assertEqual(mock_method.call_count, 1)
        self.assertEqual(len(ret), 6)
        self.assertEqual(ret[1], 'First floor')

    @patch(f'{TEST_INELS_BUS3_NAMESPACE}.getRoomDevicesRaw')
    def test_getRoomDevices_list(self, mock_method):
        """Test list of all devices in room."""
        mock_method.return_value = TEST_RAW_DEVICES

        inels = InelsBus3(TEST_HOST, TEST_PORT)
        raw = inels.getRoomDevicesRaw('room')

        self.assertEqual(mock_method.call_count, 1)
        self.assertEqual(len(raw), len(mock_method.return_value))

        # this is the way how to mock private method
        with patch.object(
            inels,
            '_InelsBus3__readDeviceData',
            return_value={'Doors_Garage': 0}
        ):
            with patch.object(inels, 'ping', return_value=True):
                json_obj = inels.getRoomDevices('room')

                device = json_obj[0]

                self.assertGreater(len(json_obj), 0)
                self.assertEqual(device.id, 'Doors_Garage')
                self.assertEqual(device.title, 'Doors')

                with patch.object(inels, 'read',
                                  return_value="{'Doors_Garage': '0'}"):
                    device_value = inels.read(device.id)
                    self.assertEqual(device_value, "{'Doors_Garage': '0'}")

    @patch(f'{TEST_INELS_BUS3_NAMESPACE}.getRooms')
    def test_getAllDevices(self, mock_method):
        """Test to load all devices in all rooms.
        We have simulation only for one room."""
        mock_method.return_value = ['Garage']

        inels = InelsBus3(TEST_HOST, TEST_PORT)

        with patch.object(
            inels,
            'getRoomDevicesRaw',
            return_value=TEST_RAW_DEVICES
        ):
            with patch.object(
                inels,
                '_InelsBus3__readDeviceData',
                return_value={'Doors_Garage': 0}
            ):
                with patch.object(inels, 'ping', return_value=True):
                    devices = inels.getAllDevices()
                    self.assertGreater(len(devices), 0)

                    lights = [x for x in devices if x.type
                              is DeviceType.LIGHT]
                    self.assertEqual(len(lights), 2)
                    garage = [x for x in devices if x.type
                              is DeviceType.GARAGE]
                    self.assertEqual(len(garage), 1)

    def test_device_type_is_in(self):
        """Test device type in inels device."""
        d_type = DeviceType.LIGHT
        d_type_res = DeviceType.is_in(d_type.value)

        self.assertEqual(d_type, d_type_res)

    def test_device_type_is_not_in(self):
        """Test device type which is not in enum."""
        d_type = "undefined_type"
        d_type_res = DeviceType.is_in(d_type)

        self.assertNotEqual(d_type, d_type_res)
        self.assertEqual(d_type_res, DeviceType.UNDEFINED)

    def test_read_bad_request(self):
        """Test observing data from device with bad response."""
        inels = InelsBus3(TEST_HOST, TEST_PORT)

        with patch.object(
            inels,
            '_InelsBus3__readDeviceData',
            return_value={'Garage_door': 0}
        ) as read:
            read.side_effect = InelsBusDataTypeException(
                "error", "bad data type")
            with self.assertRaises(InelsBusDataTypeException):
                data = inels.read('id')
                read.assert_called_once_with()
                self.assertIsNone(data)

    def test_observe_request_success(self):
        """Test observing data from devices."""
        inels = InelsBus3(TEST_HOST, TEST_PORT)

        with patch.object(
            inels,
            '_InelsBus3__readDeviceData',
            return_value={'Garage_door': 0}
        ):
            data = inels.read(['Garage_door'])
            self.assertIsNotNone(data)
            self.assertEqual(data['Garage_door'], 0)

    def test_write_bad_request(self):
        """Test write data to the proxy with bad request."""
        inels = InelsBus3(TEST_HOST, TEST_PORT)

        with patch.object(
            inels,
            '_InelsBus3__writeValues',
            return_value=None
        ) as write:
            write.side_effect = InelsBusDataTypeException(
                'write', 'Bad data type to write.')

            with self.assertRaises(InelsBusDataTypeException) as exc:
                with patch.object(inels, 'ping', return_value=True):
                    inels.write("", "")
                    exc.assert_called_once_with()
                    self.assertEqual(write.call_count, 0)

    @patch(f'{TEST_INELS_BUS3_NAMESPACE}.getRooms')
    def test_write_request_success(self, mock_method):
        """Test to write data to the proxy."""
        mock_method.return_value = ['Garage']

        inels = InelsBus3(TEST_HOST, TEST_PORT)

        with patch.object(
            inels,
            'getRoomDevicesRaw',
            return_value=TEST_RAW_DEVICES
        ):
            with patch.object(
                inels,
                '_InelsBus3__readDeviceData',
                return_value={'Doors_Garage': 0}
            ):
                with patch.object(inels, 'ping', return_value=True):
                    devices = inels.getAllDevices()
                    self.assertEqual(len(devices), 3)

                    lights = [x for x in devices if x.type is DeviceType.LIGHT]

                    with patch.object(
                        inels, '_InelsBus3__writeValues', return_value=None
                    ) as write:
                        inels.write(lights[0], 0)
                        self.assertEqual(write.call_count, 1)

    def test_InelsDevice_loadFromJson(self):
        """Testing right assigments of all properties of objects."""

        proxy = InelsBus3(TEST_HOST, TEST_PORT)

        # THERM
        therm = TEST_DATA_THERM
        therm_dev = InelsDevice(
            therm['name'], therm['therm'], DeviceType.THERM, proxy)
        therm_dev.loadFromJson(therm)

        self.assertEqual(therm['name'], therm_dev.title)
        self.assertIsNotNone(therm_dev.id)
        self.assertEqual(therm['rele'], therm_dev.rele)
        self.assertEqual(therm['therm'], therm_dev.temp_current)
        self.assertEqual(therm['stateth'], therm_dev.temp_set)
        self.assertEqual(False, therm_dev.read_only)
        self.assertEqual(DeviceType.THERM, therm_dev.type)

        # LIGHT
        therm = TEST_DATA_LIGHT
        therm_dev = InelsDevice(
            therm['name'], therm['id'], DeviceType.LIGHT, proxy)
        therm_dev.loadFromJson(therm)

        self.assertEqual(therm['name'], therm_dev.title)
        self.assertEqual(therm['id'], therm_dev.id)
        self.assertEqual(False, therm_dev.read_only)
        self.assertEqual(DeviceType.LIGHT, therm_dev.type)
        self.assertIsNone(therm_dev.rele)

        # SWITCH
        therm = TEST_DATA_SWITCH
        therm_dev = InelsDevice(
            therm['name'], therm['id'], DeviceType.SWITCH, proxy)
        therm_dev.loadFromJson(therm)

        self.assertEqual(therm['name'], therm_dev.title)
        self.assertEqual(therm['id'], therm_dev.id)
        self.assertEqual(False, therm_dev.read_only)
        self.assertEqual(DeviceType.SWITCH, therm_dev.type)
        self.assertIsNone(therm_dev.temp_current)

        # GARAGE
        therm = TEST_DATA_GARAGE
        therm_dev = InelsDevice(
            therm['name'], therm['id'], DeviceType.GARAGE, proxy)
        therm_dev.loadFromJson(therm)

        self.assertEqual(therm['name'], therm_dev.title)
        self.assertEqual(therm['id'], therm_dev.id)
        self.assertEqual(False, therm_dev.read_only)
        self.assertEqual(DeviceType.GARAGE, therm_dev.type)
        self.assertIsNone(therm_dev.temp_current)

        # HEATING
        therm = TEST_DATA_HEATING
        therm_dev = InelsDevice(
            therm['name'], therm['id'], DeviceType.HEATING, proxy)
        therm_dev.loadFromJson(therm)

        self.assertEqual(therm['name'], therm_dev.title)
        self.assertEqual(therm['id'], therm_dev.id)
        self.assertEqual(False, therm_dev.read_only)
        self.assertEqual(DeviceType.HEATING, therm_dev.type)
        self.assertIsNone(therm_dev.temp_current)

        # SHUTTER
        therm = TEST_DATA_SHUTTER
        therm_dev = InelsDevice(
            therm['name'], therm['up'], DeviceType.SHUTTER, proxy)
        therm_dev.loadFromJson(therm)

        self.assertEqual(therm['name'], therm_dev.title)
        self.assertEqual(False, therm_dev.read_only)
        self.assertEqual(therm['up'], therm_dev.up)
        self.assertEqual(therm['down'], therm_dev.down)
        self.assertEqual(DeviceType.SHUTTER, therm_dev.type)
        self.assertIsNotNone(therm_dev.id)
