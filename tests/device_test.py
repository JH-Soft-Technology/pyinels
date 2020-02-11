"""Unit testing of iNels device library."""

from tests.const_test import (
    TEST_DATA_SWITCH,
    TEST_HOST,
    TEST_INELS_BUS3_NAMESPACE,
    TEST_PORT
)

from inels.cu3 import InelsBus3
from inels.device import InelsDevice, DeviceType

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
            patch('inels.device.InelsDevice._write', return_value=None)
        ]

        self.proxy = InelsBus3(TEST_HOST, TEST_PORT)
        self.device = InelsDevice(TEST_DATA_SWITCH['name'],
                                  TEST_DATA_SWITCH['id'],
                                  DeviceType.SWITCH, self.proxy)

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
