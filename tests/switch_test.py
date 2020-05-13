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

GARAGE_RETURN_OFF = {'ZA_01_GARAGE': 0}
GARAGE_RETURN_ON = {'ZA_01_GARAGE': 1}


class PySwitchTest(TestCase):
    """Class to test iNels switch library."""

    def setUp(self):
        """Setup all necesary instances and mocks."""
        self.patches = [
            patch(f'{TEST_API_CLASS_NAMESPACE}.ping', return_value=True),
            patch(f'{TEST_API_CLASS_NAMESPACE}.getRoomDevicesRaw',
                  return_value=TEST_RAW_DEVICES),
            patch(f'{TEST_API_CLASS_NAMESPACE}._Api__readDeviceData',
                  return_value=GARAGE_RETURN_OFF),
            patch(f'{TEST_API_CLASS_NAMESPACE}._Api__writeValues',
                  return_value=None)
        ]

        for p in self.patches:
            p.start()

        self.api = Api(TEST_HOST, TEST_PORT, TEST_VERSION)
        switches = [device for device in self.api.getRoomDevices(
            'garage') if device.type == ATTR_SWITCH]

        self.switch = pySwitch(switches[0])

    def tearDown(self):
        """Destroy all instances and mocks."""
        self.api = None
        self.switch = None
        patch.stopall()
        self.patches = None

    def test_state(self):
        """Test the state of the pySwitch."""
        s = self.switch
        # the switch at the beggining should be turned off
        self.assertFalse(s.state)

    def test_unique_id_and_name_presented(self):
        """Test when the unique id is presented."""
        s = self.switch

        self.assertIsNotNone(s.unique_id)
        self.assertIsNotNone(s.name)

    def test_turn_on(self):
        """Test turn on the switch."""
        s = self.switch
        self.assertFalse(s.state)

        with patch.object(self.api, '_Api__readDeviceData',
                          return_value=GARAGE_RETURN_ON):
            s.turn_on()
            self.assertTrue(s.state)

    def test_turn_off(self):
        """Test turn off the switch."""
        s = self.switch

        with patch.object(self.api, '_Api__readDeviceData',
                          return_value=GARAGE_RETURN_ON):
            s.turn_on()
            self.assertTrue(s.state)

        s.turn_off()
        self.assertFalse(s.state)
