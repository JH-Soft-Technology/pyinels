"""Unit testing of iNels light library."""

from tests.const_test import (
    TEST_DATA_LIGHT,
    TEST_HOST,
    TEST_INELS_BUS3_NAMESPACE,
    TEST_PORT
)

from inels.cu3 import InelsBus3
from inels.device import (
    InelsDevice,
    DeviceType
)

from inels.device.InelsLight import InelsLight

from unittest.mock import patch
from unittest import TestCase


class InelsLightTest(TestCase):
    """Class to test iNels light library."""

    def setUp(self):
        """Setup all necesary instances and mocks."""
        self.patches = [
            patch(f'{TEST_INELS_BUS3_NAMESPACE}.ping', return_value=True),
            patch(f'{TEST_INELS_BUS3_NAMESPACE}.read',
                  return_value={TEST_DATA_LIGHT['id']: 1}),
            patch('inels.device.InelsDevice._write', return_value=None)
        ]

        proxy = InelsBus3(TEST_HOST, TEST_PORT)
        device = InelsDevice(TEST_DATA_LIGHT['name'],
                             TEST_DATA_LIGHT['id'],
                             DeviceType.LIGHT, proxy)

        self.light = InelsLight(device)
        # patching ping method in IneslBus3. It will be executed every test
        for p in self.patches:
            p.start()

    def tearDown(self):
        """Destroy all instances and mocks."""
        self.light = None
        patch.stopall()

    def test_initialize_light(self):
        """Initialize light test."""
        self.assertEqual(TEST_DATA_LIGHT['id'], self.light.device.id)

    def test_state_light(self):
        """Test state of the light."""
        state = self.light.state
        self.assertEqual(state, True)

    def test_has_not_brightness(self):
        """Test that the light has no brightness feature."""
        brightness_support = self.light.has_brightness
        self.assertFalse(brightness_support)

    def test_has_brightness(self):
        """Test that the light has brightness feature."""
        self.light.device.set_value(25.0)
        brightness_support = self.light.has_brightness

        self.assertTrue(brightness_support)

    def test_set_brightness(self):
        """Test set brightness of the light."""
        value = self.light.device.observe()
        # at the begining the light has no brightness support

        self.light.set_brightness(0.0)
        self.assertFalse(self.light.has_brightness)
        # no change
        self.assertEqual(value, self.light.device.value)

        # set brightness support to the light
        self.light.device.set_value(0.0)
        self.assertTrue(self.light.has_brightness)

        self.light.set_brightness(25.0)
        self.assertNotEqual(value, self.light.device.value)
        self.assertEqual(self.light.device.value, 25.0)

        self.light.set_brightness(256.0)
        # brightness is out of range, then no changes
        self.assertNotEqual(self.light.device.value, 256.0)
        self.assertEqual(self.light.device.value, 25.0)

        # remove brightness support
        self.light.device.set_value(0)
        self.assertFalse(self.light.has_brightness)
        self.light.set_brightness(25.0)
        self.assertNotEqual(self.light.device.value, 25.0)
        self.assertEqual(self.light.device.value, 0)

    def test_set_state(self):
        """Test set state of the light."""
        # set the light to turn off without brightness support
        # for testing purposes
        self.light.device.set_value(0)

        self.light.set_state()
        self.assertTrue(self.light.state)
        self.assertEqual(self.light.device.value, 1)

        # turn off the ligth
        self.light.set_state()
        self.assertFalse(self.light.state)
        self.assertEqual(self.light.device.value, 0)

        # set the brightness support
        self.light.device.set_value(0.0)
        # turn on the ligt wit brightness
        self.light.set_state()
        self.assertTrue(self.light.state)
        self.assertEqual(self.light.device.value, 255.0)
