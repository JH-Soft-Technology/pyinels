"""Unit testing of iNels door library."""

from pyinels.const import ATTR_DOOR

from tests.const_test import (
    TEST_API_CLASS_NAMESPACE,
    TEST_API_ROOM_DEVICES,
    TEST_API_READ_DATA,
    TEST_HOST,
    TEST_PORT,
    TEST_RAW_GARAGE_DOOR,
    TEST_VERSION
)

from pyinels.api import Api
from pyinels.device.pyDoor import pyDoor

from unittest.mock import patch
from unittest import TestCase


DOOR_ID = "Vrata_Garaz"
DOOR_NAME = "Vrata"

DOOR_RETURN_OFF = {DOOR_ID: 0}
DOOR_RETURN_ON = {DOOR_ID: 1}


class PyDoorTest(TestCase):
    """Class to test iNels door library."""

    def setUp(self):
        """Setup all necesary instances and mocks."""
        self.patches = [
            patch(f'{TEST_API_CLASS_NAMESPACE}.ping', return_value=True),
            patch(f'{TEST_API_CLASS_NAMESPACE}.{TEST_API_ROOM_DEVICES}',
                  return_value=TEST_RAW_GARAGE_DOOR),
            patch(f'{TEST_API_CLASS_NAMESPACE}.{TEST_API_READ_DATA}',
                  return_value=DOOR_RETURN_OFF),
            patch(f'{TEST_API_CLASS_NAMESPACE}._Api__writeValues',
                  return_value=None)
        ]

        for p in self.patches:
            p.start()

        self.api = Api(TEST_HOST, TEST_PORT, TEST_VERSION)

        doors = [device for device in self.api.getRoomDevices(
            'garage') if device.type == ATTR_DOOR]

        self.door = pyDoor(doors[0])

    def tearDown(self):
        """Destroy all instances and mocks."""
        self.api = None
        self.door = None
        patch.stopall()
        self.patches = None

    def test_state(self):
        """Test the state of the pyDoor."""
        s = self.door

        s.update()
        # the door at the beggining should be turned off
        self.assertFalse(s.state)

    def test_unique_id_and_name_presented(self):
        """Test when the unique id is presented."""
        s = self.door

        self.assertIsNotNone(s.unique_id)
        self.assertIsNotNone(s.name)

        self.assertEqual(s.unique_id, DOOR_ID)
        self.assertEqual(s.name, DOOR_NAME)

    def test_turn_on(self):
        """Test turn on the door."""
        s = self.door

        s.update()
        self.assertFalse(s.state)

        with patch.object(self.api, TEST_API_READ_DATA,
                          return_value=DOOR_RETURN_ON):
            s.turn_on()

            s.update()
            self.assertFalse(s.state)

    def test_turn_off(self):
        """Test turn off the door."""
        s = self.door

        with patch.object(self.api, TEST_API_READ_DATA,
                          return_value=DOOR_RETURN_ON):
            s.turn_on()

            s.update()
            self.assertFalse(s.state)

        s.turn_off()

        s.update()
        self.assertFalse(s.state)
