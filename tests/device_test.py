"""Unit testing of iNels device library."""
from pyinels.const import ATTR_SWITCH

from tests.const_test import (
    TEST_API_CLASS_NAMESPACE,
    TEST_HOST,
    TEST_PORT,
    TEST_RAW_DEVICES,
    TEST_VERSION
)

from pyinels.api import Api
from pyinels.device.control.switch import SwitchControl

from unittest.mock import patch
from unittest import TestCase


class DeviceTest(TestCase):
    """Class to test iNels device library."""

    def setUp(self):
        """Setup all necesary instances and mocks."""
        self.patches = [
            patch(f'{TEST_API_CLASS_NAMESPACE}.ping', return_value=True),
            patch(f'{TEST_API_CLASS_NAMESPACE}.getRoomDevicesRaw',
                  return_value=TEST_RAW_DEVICES)
        ]

        for p in self.patches:
            p.start()

        self.api = Api(TEST_HOST, TEST_PORT, TEST_VERSION)
        self.devices = self.api.getRoomDevices('garage')

    def tearDown(self):
        """Destroy all instances and mocks."""
        self.api = None
        self.devices = None
        patch.stopall()
        self.patches = None

    def test_has_switch_control(self):
        """Test when the current device has a switch control."""
        switches = [
            device for device in self.devices if device.type == ATTR_SWITCH]

        self.assertGreater(len(switches), 0)

        switch = switches[0]

        self.assertTrue(switch.has_switch_control)
        self.assertIsNotNone(switch.switch_control)
        self.assertTrue(isinstance(switch.switch_control, SwitchControl))
