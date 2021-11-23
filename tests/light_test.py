"""Unit testing of iNels light library."""
from tests.const_test import (
    TEST_API_CLASS_NAMESPACE,
    TEST_API_READ_DATA,
    TEST_API_ROOM_DEVICES,
    TEST_HOST,
    TEST_PORT,
    TEST_RAW_LIGHT,
    TEST_VERSION
)

from pyinels.const import (
    RANGE_BRIGHTNESS,
    ATTR_LIGHT
)

from pyinels.api import Api
from pyinels.device.pyLight import pyLight

from unittest.mock import patch
from unittest import TestCase

MIN_RANGE = RANGE_BRIGHTNESS[0]
MAX_RANGE = RANGE_BRIGHTNESS[1]

LIGHT_ID = 'SV_12_Garage'
LIGHT_NAME = 'Main light'

LIGHT_RETURN_OFF = {LIGHT_ID: 0}
LIGHT_RETURN_ON = {LIGHT_ID: 1}

LIGHT_RETURN_DIMMABLE_OFF = {LIGHT_ID: MIN_RANGE}
LIGHT_RETURN_DIMMABLE_ON = {LIGHT_ID: MAX_RANGE}
LIGHT_RETURN_DIMMABLE_50 = {LIGHT_ID: 50}


class PyLightTest(TestCase):
    """Class to test iNels light library."""

    def setUp(self):
        """Setup all necesary instances and mocks."""
        self.patches = [
            patch(f'{TEST_API_CLASS_NAMESPACE}.ping', return_value=True),
            patch(f'{TEST_API_CLASS_NAMESPACE}.{TEST_API_ROOM_DEVICES}',
                  return_value=TEST_RAW_LIGHT),
            patch(f'{TEST_API_CLASS_NAMESPACE}.{TEST_API_READ_DATA}',
                  return_value=LIGHT_RETURN_OFF),
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

    def test_title_and_id(self):
        """Test the name of the entity."""
        lg = self.light

        self.assertIsNotNone(lg.name)
        self.assertEqual(lg.name, LIGHT_NAME)

        self.assertIsNotNone(lg.unique_id)
        self.assertEqual(lg.unique_id, LIGHT_ID)

    def test_state(self):
        """Test the state of the pyLight."""
        lg = self.light

        lg.update()
        # the light at the beggining should be turned off
        self.assertFalse(lg.state)

    def test_unique_id_and_name_presented(self):
        """Test when the unique id is presented."""
        lg = self.light

        self.assertIsNotNone(lg.unique_id)
        self.assertIsNotNone(lg.name)

    def test_turn_on(self):
        """Test turn on the light."""
        lg = self.light

        lg.update()
        self.assertFalse(lg.state)

        with patch.object(self.api, TEST_API_READ_DATA,
                          return_value=LIGHT_RETURN_ON):
            lg.turn_on()

            lg.update()
            self.assertTrue(lg.state)

        lg.turn_off()

        lg.update()
        self.assertFalse(lg.state)

    def test_turn_off(self):
        """Test turn off the light."""
        lg = self.light

        with patch.object(self.api, TEST_API_READ_DATA,
                          return_value=LIGHT_RETURN_ON):
            lg.turn_on()

            lg.update()
            self.assertTrue(lg.state)

        lg.turn_off()

        lg.update()
        self.assertFalse(lg.state)


class PyLightDimmableTest(TestCase):
    """Class to test iNels light library."""

    def setUp(self):
        """Setup all necesary instances and mocks."""
        self.patches = [
            patch(f'{TEST_API_CLASS_NAMESPACE}.ping', return_value=True),
            patch(f'{TEST_API_CLASS_NAMESPACE}.{TEST_API_ROOM_DEVICES}',
                  return_value=TEST_RAW_LIGHT),
            patch(f'{TEST_API_CLASS_NAMESPACE}.{TEST_API_READ_DATA}',
                  return_value=LIGHT_RETURN_DIMMABLE_OFF),
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

    def test_turn_on_with_brightness_option(self):
        """Test the light to turn on when the brightness exists."""

        lg = self.light

        lg.update()
        self.assertFalse(lg.state)
        self.assertTrue(lg.has_brightness)

        with patch.object(self.api, TEST_API_READ_DATA,
                          return_value=LIGHT_RETURN_DIMMABLE_ON):
            lg.turn_on()

            lg.update()
            self.assertTrue(lg.state)

    def test_set_brightness_to_50_percent(self):
        """Test the brightnes to some value."""

        lg = self.light

        lg.update()
        self.assertFalse(lg.state)
        self.assertTrue(lg.has_brightness)

        with patch.object(self.api, TEST_API_READ_DATA,
                          return_value=LIGHT_RETURN_DIMMABLE_50):

            lg.set_brightness(50)

            self.assertEqual(lg.brightness(), 50)
            self.assertTrue(lg.state)

    @patch(f'{TEST_API_CLASS_NAMESPACE}.{TEST_API_READ_DATA}')
    def test_turn_off_with_brightness_option(self, mock_room_devices):
        """Test the light to turn off when the brightness exsists."""
        mock_room_devices.return_value = LIGHT_RETURN_DIMMABLE_ON

        lg = self.light

        self.assertTrue(lg.has_brightness)

        lg.update()
        self.assertTrue(lg.state)

        with patch.object(self.api, TEST_API_READ_DATA,
                          return_value=LIGHT_RETURN_DIMMABLE_OFF):
            lg.turn_off()
            self.assertTrue(lg.has_brightness)

            lg.update()
            self.assertFalse(lg.state)
