"""Unit testing of iNels shutter library."""
from pyinels.const import (
    ATTR_SHUTTER,
    STATE_CLOSED,
    STATE_CLOSING,
    STATE_OPEN,
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
    TEST_RETURN_RESOURCE_SHUTTER_UP,
    TEST_RETURN_RESOURCE_SHUTTER_DOWN
)

from time import sleep
from pyinels.api import Api
from pyinels.device.pyShutter import pyShutter

from unittest.mock import patch
from unittest import TestCase


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

    def test_closed_state(self):
        """Test the state of the pyShutter."""
        shutt = self.shutter

        shutt.update()
        # the shutter at the beggining should be turned off
        self.assertIs(shutt.state, STATE_CLOSED)

    def test_unique_id_and_name_presented(self):
        """Test when the unique id is presented."""
        shutt = self.shutter

        self.assertIsNotNone(shutt.unique_id)
        self.assertIsNotNone(shutt.name)

        self.assertEqual(shutt.unique_id, TEST_SHUTTER_ID)
        self.assertEqual(shutt.name, TEST_SHUTTER_NAME)

    def test_full_opening(self):
        """Test full open shutter."""
        shutt = self.shutter

        shutt.pull_up(2)

        with patch.object(self.api, TEST_API_READ_DATA,
                          return_value=TEST_RETURN_RESOURCE_SHUTTER_UP):

            self.assertFalse(shutt.should_stop)
            self.assertEqual(shutt.state, STATE_OPENING)

            sleep(1)
            self.assertFalse(shutt.should_stop)
            self.assertEqual(shutt.state, STATE_OPENING)

            sleep(1)
            self.assertTrue(shutt.should_stop)
            self.assertEqual(shutt.state, STATE_OPEN)

    def test_full_close(self):
        """Test to full close the shutter."""
        shutt = self.shutter

        shutt.pull_down(2)

        with patch.object(self.api, TEST_API_READ_DATA,
                          return_value=TEST_RETURN_RESOURCE_SHUTTER_DOWN):

            self.assertFalse(shutt.should_stop)
            self.assertEqual(shutt.state, STATE_CLOSING)

            sleep(1)
            self.assertFalse(shutt.should_stop)
            self.assertEqual(shutt.state, STATE_CLOSING)

            sleep(1)
            self.assertTrue(shutt.should_stop)
            self.assertEqual(shutt.state, STATE_CLOSED)
