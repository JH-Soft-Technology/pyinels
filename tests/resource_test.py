"""Resource testing."""
from unittest.mock import patch
from unittest import TestCase

from pyinels.api import Api
from pyinels.api.resources import ApiResource
from tests.const_test import (
    TEST_API_CLASS_NAMESPACE,
    TEST_API_NAMESPACE,
    TEST_API_ROOM_DEVICES,
    TEST_API_READ_DATA,
    TEST_HOST,
    TEST_PORT,
    TEST_RAW_GARAGE_DOOR,
    TEST_RESOURCE_SWITCH,
    TEST_VERSION
)

GARAGE_ID = "Vrata_Garaz"
GARAGE_NAME = "Vrata"

GARAGE_CLOSE = {GARAGE_ID: 0}
GARAGE_OPEN = {GARAGE_ID: 1}


class ResourceTest(TestCase):
    """Class to test resource of api iNels BUS."""

    def setUp(self):
        self.api = Api(TEST_HOST, TEST_PORT, TEST_VERSION)

        self.patches = [
            patch(f'{TEST_API_CLASS_NAMESPACE}.ping', return_value=True),
            patch(f'{TEST_API_CLASS_NAMESPACE}.{TEST_API_ROOM_DEVICES}',
                  return_value=TEST_RAW_GARAGE_DOOR),
            patch(f'{TEST_API_CLASS_NAMESPACE}.{TEST_API_READ_DATA}',
                  return_value=GARAGE_CLOSE)
        ]

        for p in self.patches:
            p.start()

        self.res_list = self.api.getRoomDevices('garage')
        self.garage_door = self.res_list[0]

    def tearDown(self):
        """Destroy all instances and mocks."""
        self.api = None
        self.res_list = None
        self.garage_door = None
        patch.stopall()
        self.patches = None

    @patch(f'{TEST_API_NAMESPACE}.resources.ApiResource')
    def test_load_resource_object(self, mock_class):
        """Test to load resource object."""
        mock_class(TEST_RESOURCE_SWITCH, self.api)

        mock_class.assert_called()
        mock_class.assert_called_once()

        self.assertEqual(mock_class.call_count, 1)

        res = ApiResource(TEST_RESOURCE_SWITCH, self.api)

        self.assertIsInstance(res, ApiResource)

        self.assertEqual(TEST_RESOURCE_SWITCH['type'], res.type)
        # inels is raw data id from iNels BUS
        self.assertEqual(TEST_RESOURCE_SWITCH['inels'], res.id)
        self.assertEqual(TEST_RESOURCE_SWITCH['name'], res.title)
        self.assertEqual(TEST_RESOURCE_SWITCH['read_only'], res.read_only)
        # should be none, because it does not get the observe
        self.assertIsNone(res.value)

    @patch(f'{TEST_API_CLASS_NAMESPACE}.read')
    def test_observe(self, mock_room_devices):
        """Test the observe method of the Api resources. It should touche
        the iNels BUS."""
        mock_room_devices.return_value = GARAGE_CLOSE

        self.assertEqual(len(self.res_list), 1)
        self.assertEqual(self.garage_door.title, GARAGE_NAME)

        door = self.garage_door.observe()
        value = door[self.garage_door.id]

        self.assertEqual(value, 0)

        self.assertIsNotNone(self.garage_door.value)
        self.assertEqual(self.garage_door.value[self.garage_door.id], 0)

    def test_write_value(self):
        """Test set value to the iNels BUS."""
        with patch.object(self.api, '_Api__writeValues', return_value=None):
            # set int
            self.garage_door.write_value(1)
            self.assertEqual(self.garage_door.value[self.garage_door.id], '1')

            # change int to another value
            self.garage_door.write_value(0)
            self.assertEqual(self.garage_door.value[self.garage_door.id], '0')

            # change to float with different value
            self.garage_door.write_value(25.0)
            self.assertEqual(
                self.garage_door.value[self.garage_door.id], '25.0')

            # change to int with same value
            self.garage_door.write_value(25)
            self.assertEqual(self.garage_door.value[self.garage_door.id], '25')

    @patch(f'{TEST_API_CLASS_NAMESPACE}.{TEST_API_READ_DATA}')
    def test_is_available(self, mock_garage_object):
        mock_garage_object.return_value = None

        """Test when the resource object is available."""
        with patch.object(self.api, '_Api__writeValues', return_value=None):
            # set the value of the ApiResource then it should be available
            self.garage_door.write_value(1)
            self.assertTrue(self.garage_door.is_available)
