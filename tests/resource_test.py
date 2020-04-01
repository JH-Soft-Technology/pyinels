"""Resource testing."""
from unittest import TestCase
from unittest.mock import patch

from pyinels.api import Api
from pyinels.api.resources import ApiResource
from tests.const_test import (
    TEST_API_NAMESPACE,
    TEST_HOST,
    TEST_PORT,
    TEST_RESOURCE_SWITCH,
    TEST_VERSION
)


class ResourceTest(TestCase):
    """Class to test resource of api iNels BUS."""

    def setUp(self):
        self.api = Api(TEST_HOST, TEST_PORT, TEST_VERSION)

    def tearDown(self):
        """Destroy all instances and mocks."""
        self.api = None

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
