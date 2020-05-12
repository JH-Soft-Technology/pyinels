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
        self.lights = [device for device in self.api.getRoomDevices(
            'garage') if device.type == ATTR_LIGHT]

        self.light = pyLight(self.lights[0])

    def tearDown(self):
        """Destroy all instances and mocks."""
        self.api = None
        self.light = None
        self.lights = []
        patch.stopall()
        self.patches = None

    def test_state(self):
        """Test the state of the pyLight."""
        l = self.light
        # the light at the beggining should be turned off
        self.assertFalse(l.state)

    def test_unique_id_and_name_presented(self):
        """Test when the unique id is presented."""
        l = self.light

        self.assertIsNotNone(l.unique_id)
        self.assertIsNotNone(l.name)

    def test_turn_on(self):
        """Test turn on the light."""
        l = self.light

        self.assertFalse(l.state)
        l.turn_on()
        self.assertTrue(l.state)

        l.turn_off()
        self.assertFalse(l.state)

    def test_turn_off(self):
        """Test turn off the light."""
        l = self.light
        l.turn_on()
        self.assertTrue(l.state)

        l.turn_off()
        self.assertFalse(l.state)

    @patch(f'{TEST_API_CLASS_NAMESPACE}._Api__readDeviceData')
    def test_turn_on_with_brightness_option(self, mock_room_devices):
        """Test the light to turn on when the brightness 
        is presented."""
        mock_room_devices.return_value = {'SV_Wall_Garage': 0.0}

        l = pyLight(self.lights[1])
        self.assertTrue(l.has_brightness,
                        "The light does not have a brightness")
        self.assertFalse(l.state, "The light is not turned off")

        l.turn_on()
        self.assertTrue(l.state, "The light is not turned on")
