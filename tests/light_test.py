"""Unit testing of iNels light library."""

from pyinels.const import ATTR_LIGHT

from tests.const_test import (
    TEST_API_CLASS_NAMESPACE,
    TEST_HOST,
    TEST_PORT,
    TEST_RAW_DEVICES,
    TEST_VERSION
)

from pyinels.api import Api
from pyinels.device.pyLight import pyLight

from unittest.mock import patch
from unittest import TestCase


class PyLightTest(TestCase):
    """Class to test iNels light library."""

    def setUp(self):
        """Setup all necesary instances and mocks."""
        self.patches = [
            patch(f'{TEST_API_CLASS_NAMESPACE}.ping', return_value=True),
            patch(f'{TEST_API_CLASS_NAMESPACE}.getRoomDevicesRaw',
                  return_value=TEST_RAW_DEVICES),
            patch(f'{TEST_API_CLASS_NAMESPACE}._Api__readDeviceData',
                  return_value={'SV_12_Garage': 0}),
            patch(f'{TEST_API_CLASS_NAMESPACE}._Api__writeValues',
                  return_value=None)
        ]

        for p in self.patches:
            p.start()

        self.api = Api(TEST_HOST, TEST_PORT, TEST_VERSION)
        lights = [device for device in self.api.getRoomDevices(
            'garage') if device.type == ATTR_LIGHT]

        self.light = pyLight(lights[0])

    def tearDown(self):
        """Destroy all instances and mocks."""
        self.api = None
        self.light = None
        patch.stopall()
        self.patches = None

    def test_state(self):
        """Test the state of the pyLight."""
        s = self.light
        # the light at the beggining should be turned off
        self.assertFalse(s.state)

    def test_unique_id_and_name_presented(self):
        """Test when the unique id is presented."""
        s = self.light

        self.assertIsNotNone(s.unique_id)
        self.assertIsNotNone(s.name)

    def test_turn_on(self):
        """Test turn on the light."""
        s = self.light

        self.assertFalse(s.state)
        s.turn_on()
        self.assertTrue(s.state)

    def test_turn_off(self):
        """Test turn off the light."""
        s = self.light
        s.turn_on()
        self.assertTrue(s.state)

        s.turn_off()
        self.assertFalse(s.state)
