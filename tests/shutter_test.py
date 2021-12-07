"""Unit testing of iNels shutter library."""

# import asyncio

from unittest.mock import patch
from unittest import TestCase

from pyinels.api import Api
from pyinels.device.pyShutter import pyShutter

from pyinels.const import (
    ATTR_SHUTTER,
    STATE_CLOSED,
    STATE_OPEN,
    STATE_CLOSING,
    STATE_OPENING
)

from tests.const_test import (
    TEST_API_CLASS_NAMESPACE,
    TEST_API_ROOM_DEVICES,
    TEST_API_READ_DATA,
    TEST_HOST,
    TEST_PORT,
    TEST_RAW_SHUTTER,
    TEST_VERSION,
    TEST_SHUTTER_UP,
    TEST_SHUTTER_DOWN,
    TEST_SHUTTER_ID,
    TEST_SHUTTER_NAME,
    TEST_RETURN_RESOURCE_SHUTTER,
)


SHUTTER_UP_ON = {TEST_SHUTTER_UP: 1}
SHUTTER_UP_OFF = {TEST_SHUTTER_UP: 0}

SHUTTER_DOWN_ON = {TEST_SHUTTER_DOWN: 1}
SHUTTER_DOWN_OFF = {TEST_SHUTTER_DOWN: 0}


class PyShutterTest(TestCase):
    """Class to test iNels shutter library."""

    def setUp(self):
        """Setup all necesary instances and mocks."""
        self.patches = [
            patch(f'{TEST_API_CLASS_NAMESPACE}.ping', return_value=True),
            patch(f'{TEST_API_CLASS_NAMESPACE}.{TEST_API_ROOM_DEVICES}',
                  return_value=TEST_RAW_SHUTTER),
            patch(f'{TEST_API_CLASS_NAMESPACE}.{TEST_API_READ_DATA}',
                  return_value=TEST_RETURN_RESOURCE_SHUTTER),
            patch(f'{TEST_API_CLASS_NAMESPACE}._Api__writeValues',
                  return_value=None)
        ]

        for item in self.patches:
            item.start()

        self.api = Api(TEST_HOST, TEST_PORT, TEST_VERSION)

        shutters = [device for device in self.api.getRoomDevices(
            'garage') if device.type == ATTR_SHUTTER]

        self.shutter = pyShutter(shutters[0])

    def tearDown(self):
        """Destroy all instances and mocks."""
        self.api = None
        self.shutter = None
        patch.stopall()
        self.patches = None

    def test_state_after_initialization(self):
        """Test the state of the pyShutter."""
        shutt = self.shutter

        shutt.update()
        # the shutter at the beggining should be open. There will be
        # calibration
        self.assertIs(shutt.state, STATE_OPEN)

    def test_opening(self):
        """Check up and down when opening."""
        shutt = self.shutter

        shutt.pull_up()

        self.assertEqual(shutt.up, 1)
        self.assertEqual(shutt.down, 0)
        self.assertEqual(shutt.current_position, 100)
        self.assertEqual(shutt.state, STATE_OPENING)

        shutt.stop()

        self.assertEqual(shutt.up, 0)
        self.assertEqual(shutt.down, 0)
        self.assertEqual(shutt.current_position, 100)
        self.assertEqual(shutt.state, STATE_OPEN)

    def test_closing(self):
        """Check up and down when closing."""
        shutt = self.shutter

        shutt.pull_down()

        self.assertEqual(shutt.up, 0)
        self.assertEqual(shutt.down, 1)
        self.assertEqual(shutt.current_position, 0)
        self.assertEqual(shutt.state, STATE_CLOSING)

        shutt.stop()

        self.assertEqual(shutt.up, 0)
        self.assertEqual(shutt.down, 0)
        self.assertEqual(shutt.current_position, 0)
        self.assertEqual(shutt.state, STATE_CLOSED)

    def test_unique_id_and_name_presented(self):
        """Test when the unique id is presented."""
        shutt = self.shutter

        self.assertIsNotNone(shutt.unique_id)
        self.assertIsNotNone(shutt.name)

        self.assertEqual(shutt.unique_id, TEST_SHUTTER_ID)
        self.assertEqual(shutt.name, TEST_SHUTTER_NAME)
