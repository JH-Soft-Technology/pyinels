"""Unit testing of iNels switch library."""
from pyinels.const import ATTR_SWITCH

from tests.const_test import (
    TEST_API_CLASS_NAMESPACE,
    TEST_HOST,
    TEST_PORT,
    TEST_RAW_DEVICES,
    TEST_VERSION
)

from pyinels.api import Api
from pyinels.device.pySwitch import pySwitch

from unittest.mock import patch
from unittest import TestCase


class PySwitchTest(TestCase):
    """Class to test iNels switch library."""

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
        switches = [device for device in self.api.getRoomDevices(
            'garage') if device.type == ATTR_SWITCH]

        self.device = switches[0]

    def tearDown(self):
        """Destroy all instances and mocks."""
        self.api = None
        self.device = None
        patch.stopall()
        self.patches = None

    def test_state(self):
        """Test the state of the pySwitch."""
        with patch.object(self.api, '_Api__readDeviceData',
                          return_value={'ZA_01_GARAGE': 0}):
            p = pySwitch(self.device)

            # the switch at the beggining should be turned off
            self.assertFalse(p.state)

            with patch.object(self.api, '_Api__writeValues',
                              return_value=None):
                # tur on the switch
                p.turn_on()

                self.assertTrue(p.state)
