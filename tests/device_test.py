"""Unit testing of iNels device library."""
from tests.const_test import (
    TEST_DATA_SWITCH,
    TEST_HOST,
    TEST_INELS_BUS3_NAMESPACE,
    TEST_INELS_DEVICE_NAMESPACE,
    TEST_PORT
)

from pyinels.exception import InelsBusClassTypeException
from pyinels.cu3 import InelsBus3
from pyinels.device import (
    InelsDevice,
    DeviceType,
    Observe
)

from unittest.mock import patch
from unittest import TestCase


class DeviceTest(TestCase):
    """Class to test iNels device library."""

    def setUp(self):
        """Setup all necesary instances and mocks."""
        self.patches = [
            patch(f'{TEST_INELS_BUS3_NAMESPACE}.ping', return_value=True),
            patch(f'{TEST_INELS_BUS3_NAMESPACE}.read',
                  return_value={TEST_DATA_SWITCH['id']: 1}),
            patch(f'{TEST_INELS_DEVICE_NAMESPACE}._write', return_value=None)
        ]

        self.proxy = InelsBus3(TEST_HOST, TEST_PORT)
        self.device = InelsDevice(TEST_DATA_SWITCH['name'],
                                  TEST_DATA_SWITCH['id'],
                                  DeviceType.is_in("on_off"), self.proxy)

        # patching ping method in IneslBus3. It will be executed every test
        for p in self.patches:
            p.start()

    def tearDown(self):
        """Destroy all instances and mocks."""
        self.proxy = None
        self.device = None
        patch.stopall()

    def test_initialize_device(self):
        """Class instance test."""
        self.assertEqual(True, self.proxy.ping())

        self.device.loadFromJson(TEST_DATA_SWITCH)

        self.assertEqual(TEST_DATA_SWITCH['name'], self.device.title)
        self.assertEqual(TEST_DATA_SWITCH['id'], self.device.id)
        self.assertEqual(self.device.value, None)

    def test_observer_device(self):
        """Test the observer value of the device."""
        dev_value = self.device.observe()
        self.assertEqual(1, dev_value)
        self.assertEqual(1, self.device.value)

    def test_set_value_device(self):
        """Test setting the value of the device."""
        self.device.set_value(0)
        self.assertEqual(0, self.device.value)

    def test_device_type_is_in(self):
        """Test device type in inels device."""
        d_type = DeviceType.LIGHT
        d_type_res = DeviceType.is_in(d_type.value)

        self.assertEqual(d_type.value, d_type_res)

    def test_device_type_is_not_in(self):
        """Test device type which is not in enum."""
        d_type = "undefined_type"
        d_type_res = DeviceType.is_in(d_type)

        self.assertNotEqual(d_type, d_type_res)
        self.assertEqual(d_type_res, DeviceType.UNDEFINED.value)

    def test_observe_request_success(self):
        """Test observing data from devices."""

        data = self.proxy.read(['KITCHEN_KETTLE_SWITCH'])
        self.assertIsNotNone(data)
        self.assertEqual(data['KITCHEN_KETTLE_SWITCH'], 1)

    def test_observe_with_callback(self):
        """Test observing data form device with callback function."""
        class Dev:
            def __init__(self):
                self.name = "Default Dev class name"
                self.device = None

        dev = Dev()

        self.assertIsNone(dev.device)

        def _observe_update(device):
            """Observe update fnc."""
            dev.device = device
            dev.name = device.title

        def _error(self):
            return self.test_observe_with_callback()

        cmd = Observe(_observe_update, _error)

        self.assertNotEqual(self.device.title, dev.name)

        self.device.observe(cmd)
        self.assertIsNotNone(dev.device)

        self.assertEqual(self.device.title, dev.name)
        self.assertEqual(self.device.value, 1)

        self.device.set_value(0)
        self.assertEqual(self.device.value, 0)

        self.device.observe(cmd)  # will read data from mock, so value = 1
        self.assertEqual(self.device.value, 1)

    def test_observe_requiest_with_bad_options_type(self):
        """Test the device observe."""
        observedValue = None

        with self.assertRaises(InelsBusClassTypeException):
            observedValue = self.device.observe("bad options")

        self.assertIsNone(observedValue)

    # def test_device_json_serializable(self):
    #     """Test the device json serialize."""
    #     serialized = json.dumps(self.device.__dict__)

    #     self.assertIsNotNone(serialized)
