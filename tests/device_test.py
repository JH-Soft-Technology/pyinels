"""Unit testing of iNels device library."""
from tests.const_test import (
    TEST_API_CLASS_NAMESPACE,
    TEST_HOST,
    TEST_PORT,
    TEST_VERSION
)

from pyinels.api import Api

from unittest.mock import patch
from unittest import TestCase


class DeviceTest(TestCase):
    """Class to test iNels device library."""

    def setUp(self):
        """Setup all necesary instances and mocks."""
        self.patches = [
            patch(f'{TEST_API_CLASS_NAMESPACE}.ping', return_value=True)
        ]

        self.api = Api(TEST_HOST, TEST_PORT, TEST_VERSION)

        # patching ping method in IneslBus3. It will be executed every test
        for p in self.patches:
            p.start()

    def tearDown(self):
        """Destroy all instances and mocks."""
        self.api = None
        patch.stopall()
