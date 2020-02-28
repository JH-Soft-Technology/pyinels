"""Unit testing of iNels BUS CU3 library."""

from tests.const_test import (
    TEST_HOST,
    TEST_INELS_BUS3_NAMESPACE,
    TEST_INELS_DEVICE_NAMESPACE,
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
from pyinels.cu3 import (
    InelsBus3,
    InelsBusException,
    InelsBusDataTypeException,
)
from pyinels.device import (
    DeviceType,
    InelsDevice
)

from pyinels.device.pySwitch import pySwitch
from unittest.mock import patch, Mock
from unittest import TestCase


class InelsBus3Test(TestCase):
    """Class to test iNels BUS CU3 library."""

    def setUp(self):
        """Setup all necessary instances nad mocks."""
        self.patches = [
            patch(f'{TEST_INELS_BUS3_NAMESPACE}.ping', return_value=True),
            patch(f'{TEST_INELS_BUS3_NAMESPACE}.read',
                  return_value={TEST_DATA_SWITCH['id']: 1}),
            patch(f'{TEST_INELS_DEVICE_NAMESPACE}._write', return_value=None)
        ]

        self.proxy = InelsBus3(TEST_HOST, TEST_PORT)
        self.device = InelsDevice(TEST_DATA_SWITCH['name'],
                                  TEST_DATA_SWITCH['id'],
                                  DeviceType.SWITCH, self.proxy)

        self.switch = pySwitch(self.device)
        # patching ping method in IneslBus3. It will be executed every test
        for p in self.patches:
            p.start()

    def tearDown(self):
        """Destroy all instances and mocks."""
        self.proxy = None
        self.device = None
        self.switch = None
        patch.stopall()

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

        ret = self.proxy.ping()
        self.assertEqual(True, ret)
        self.assertEqual(mock_server.call_count, 0)

    @patch(f'{TEST_INELS_BUS3_NAMESPACE}.ping')
    def test_ping_failed(self, mock_method):
        """Test ping method."""
        mock_method.return_value = False
        ret = self.proxy.ping()

        self.assertEqual(mock_method.call_count, 1)
        self.assertFalse(ret)

    @patch(f'{TEST_INELS_BUS3_NAMESPACE}.getPlcIp')
    def test_getPlcIp_success(self, mock_method):
        """Test Ip address of the PLC."""
        mock_method.return_value = "192.168.2.10"

        ret = self.proxy.getPlcIp()

        self.assertEqual(mock_method.call_count, 1)
        self.assertEqual(ret, "192.168.2.10")

    @patch(f'{TEST_INELS_BUS3_NAMESPACE}.getRooms')
    def test_getRoomsRaw_list(self, mock_method):
        """Test list of rooms defined on Connection server."""
        mock_method.return_value = TEST_ROOMS

        ret = self.proxy.getRooms()

        self.assertEqual(mock_method.call_count, 1)
        self.assertEqual(len(ret), 6)
        self.assertEqual(ret[1], 'First floor')

    @patch(f'{TEST_INELS_BUS3_NAMESPACE}.getRoomDevicesRaw')
    def test_getRoomDevices_list(self, mock_method):
        """Test list of all devices in room."""
        mock_method.return_value = TEST_RAW_DEVICES
        raw = self.proxy.getRoomDevicesRaw('room')

        self.assertEqual(mock_method.call_count, 1)
        self.assertEqual(len(raw), len(mock_method.return_value))

        # this is the way how to mock private method
        with patch.object(
            self.proxy,
            '_InelsBus3__readDeviceData',
            return_value={'Doors_Garage': 0}
        ):
            with patch.object(self.proxy, 'ping', return_value=True):
                json_obj = self.proxy.getRoomDevices('room')

                device = json_obj[0]

                self.assertGreater(len(json_obj), 0)
                self.assertEqual(device.id, 'Doors_Garage')
                self.assertEqual(device.title, 'Doors')

                with patch.object(self.proxy, 'read',
                                  return_value="{'Doors_Garage': '0'}"):
                    device_value = self.proxy.read(device.id)
                    self.assertEqual(device_value, "{'Doors_Garage': '0'}")

    @patch(f'{TEST_INELS_BUS3_NAMESPACE}.getRooms')
    def test_getAllDevices(self, mock_method):
        """Test to load all devices in all rooms.
        We have simulation only for one room."""
        mock_method.return_value = ['Garage']

        with patch.object(
            self.proxy,
            'getRoomDevicesRaw',
            return_value=TEST_RAW_DEVICES
        ):
            with patch.object(
                self.proxy,
                '_InelsBus3__readDeviceData',
                return_value={'Doors_Garage': 0}
            ):
                with patch.object(self.proxy, 'ping', return_value=True):
                    devices = self.proxy.getAllDevices()
                    self.assertGreater(len(devices), 0)

                    lights = [x for x in devices if x.type
                              is DeviceType.LIGHT]
                    self.assertEqual(len(lights), 2)
                    garage = [x for x in devices if x.type
                              is DeviceType.GARAGE]
                    self.assertEqual(len(garage), 1)

    def test_read_bad_request(self):
        """Test observing data from device with bad response."""
        patch.stopall()  # need to stop all patches for this test
        cu = InelsBus3(TEST_HOST, TEST_PORT)

        with patch.object(
            cu,
            '_InelsBus3__readDeviceData',
            return_value={'Garage_door': 0}
        ) as read:
            read.side_effect = InelsBusDataTypeException(
                "error", "bad data type")
            with self.assertRaises(InelsBusDataTypeException):
                data = cu.read('id')
                read.assert_called_once_with()
                self.assertIsNone(data)

    def test_write_bad_request(self):
        """Test write data to the proxy with bad request."""
        with patch.object(
            self.proxy,
            '_InelsBus3__writeValues',
            return_value=None
        ) as write:
            write.side_effect = InelsBusDataTypeException(
                'write', 'Bad data type to write.')

            with self.assertRaises(InelsBusDataTypeException) as exc:
                with patch.object(self.proxy, 'ping', return_value=True):
                    self.proxy.write("", "")
                    exc.assert_called_once_with()
                    self.assertEqual(write.call_count, 0)

    @patch(f'{TEST_INELS_BUS3_NAMESPACE}.getRooms')
    def test_write_request_success(self, mock_method):
        """Test to write data to the proxy."""
        mock_method.return_value = ['Garage']

        with patch.object(
            self.proxy,
            'getRoomDevicesRaw',
            return_value=TEST_RAW_DEVICES
        ):
            with patch.object(
                self.proxy,
                '_InelsBus3__readDeviceData',
                return_value={'Doors_Garage': 0}
            ):
                with patch.object(self.proxy, 'ping', return_value=True):
                    devices = self.proxy.getAllDevices()
                    self.assertEqual(len(devices), 3)

                    lights = [x for x in devices if x.type is DeviceType.LIGHT]

                    with patch.object(
                        self.proxy, '_InelsBus3__writeValues',
                        return_value=None
                    ) as write:
                        self.proxy.write(lights[0], 0)
                        self.assertEqual(write.call_count, 1)

    def test_InelsDevice_loadFromJson(self):
        """Testing right assigments of all properties of objects."""

        # THERM
        therm = TEST_DATA_THERM
        therm_dev = InelsDevice(
            therm['name'], therm['therm'], DeviceType.THERM, self.proxy)
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
            therm['name'], therm['id'], DeviceType.LIGHT, self.proxy)
        therm_dev.loadFromJson(therm)

        self.assertEqual(therm['name'], therm_dev.title)
        self.assertEqual(therm['id'], therm_dev.id)
        self.assertEqual(False, therm_dev.read_only)
        self.assertEqual(DeviceType.LIGHT, therm_dev.type)
        self.assertIsNone(therm_dev.rele)

        # SWITCH
        therm = TEST_DATA_SWITCH
        therm_dev = InelsDevice(
            therm['name'], therm['id'], DeviceType.SWITCH, self.proxy)
        therm_dev.loadFromJson(therm)

        self.assertEqual(therm['name'], therm_dev.title)
        self.assertEqual(therm['id'], therm_dev.id)
        self.assertEqual(False, therm_dev.read_only)
        self.assertEqual(DeviceType.SWITCH, therm_dev.type)
        self.assertIsNone(therm_dev.temp_current)

        # GARAGE
        therm = TEST_DATA_GARAGE
        therm_dev = InelsDevice(
            therm['name'], therm['id'], DeviceType.GARAGE, self.proxy)
        therm_dev.loadFromJson(therm)

        self.assertEqual(therm['name'], therm_dev.title)
        self.assertEqual(therm['id'], therm_dev.id)
        self.assertEqual(False, therm_dev.read_only)
        self.assertEqual(DeviceType.GARAGE, therm_dev.type)
        self.assertIsNone(therm_dev.temp_current)

        # HEATING
        therm = TEST_DATA_HEATING
        therm_dev = InelsDevice(
            therm['name'], therm['id'], DeviceType.HEATING, self.proxy)
        therm_dev.loadFromJson(therm)

        self.assertEqual(therm['name'], therm_dev.title)
        self.assertEqual(therm['id'], therm_dev.id)
        self.assertEqual(False, therm_dev.read_only)
        self.assertEqual(DeviceType.HEATING, therm_dev.type)
        self.assertIsNone(therm_dev.temp_current)

        # SHUTTER
        therm = TEST_DATA_SHUTTER
        therm_dev = InelsDevice(
            therm['name'], therm['up'], DeviceType.SHUTTER, self.proxy)
        therm_dev.loadFromJson(therm)

        self.assertEqual(therm['name'], therm_dev.title)
        self.assertEqual(False, therm_dev.read_only)
        self.assertEqual(therm['up'], therm_dev.up)
        self.assertEqual(therm['down'], therm_dev.down)
        self.assertEqual(DeviceType.SHUTTER, therm_dev.type)
        self.assertIsNotNone(therm_dev.id)
