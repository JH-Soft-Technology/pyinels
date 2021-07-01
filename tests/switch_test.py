"""Unit testing of iNels switch library."""
from pyinels.const import ATTR_SWITCH

from tests.const_test import (
    TEST_API_CLASS_NAMESPACE,
    TEST_API_ROOM_DEVICES,
    TEST_API_READ_DATA,
    TEST_HOST,
    TEST_PORT,
    TEST_RAW_SWITCH,
    TEST_VERSION
)

from pyinels.api import Api
from pyinels.device.pySwitch import pySwitch

from unittest.mock import patch
from unittest import async_case

SWITCH_ID = "ZAS_13A_Loznice"
SWITCH_NAME = "Zas loznice"

SWITCH_RETURN_OFF = {SWITCH_ID: 0}
SWITCH_RETURN_ON = {SWITCH_ID: 1}


class PySwitchTest(async_case.IsolatedAsyncioTestCase):
    """Class to test iNels switch library."""

    def setUp(self):
        """Setup all necesary instances and mocks."""
        self.patches = [
            patch(f'{TEST_API_CLASS_NAMESPACE}.ping', return_value=True),
            patch(f'{TEST_API_CLASS_NAMESPACE}.{TEST_API_ROOM_DEVICES}',
                  return_value=TEST_RAW_SWITCH),
            patch(f'{TEST_API_CLASS_NAMESPACE}.{TEST_API_READ_DATA}',
                  return_value=SWITCH_RETURN_OFF),
            patch(f'{TEST_API_CLASS_NAMESPACE}._Api__writeValues',
                  return_value=None)
        ]

        for p in self.patches:
            p.start()

        self.api = Api(TEST_HOST, TEST_PORT, TEST_VERSION)

    async def asyncSetUp(self):
        """Setup all neccessary async stuff."""
        switches = [device for device in await self.api.getRoomDevices(
            'garage') if device.type == ATTR_SWITCH]

        self.switch = await pySwitch(switches[0])

    def tearDown(self):
        """Destroy all instances and mocks."""
        self.api = None
        self.switch = None
        patch.stopall()
        self.patches = None

    async def test_state(self):
        """Test the state of the pySwitch."""
        s = self.switch

        await s.update()
        # the switch at the beggining should be turned off
        self.assertFalse(s.state)

    def test_unique_id_and_name_presented(self):
        """Test when the unique id is presented."""
        s = self.switch

        self.assertIsNotNone(s.unique_id)
        self.assertIsNotNone(s.name)

        self.assertEqual(s.unique_id, SWITCH_ID)
        self.assertEqual(s.name, SWITCH_NAME)

    async def test_turn_on(self):
        """Test turn on the switch."""
        s = self.switch

        await s.update()
        self.assertFalse(s.state)

        with patch.object(self.api, TEST_API_READ_DATA,
                          return_value=SWITCH_RETURN_ON):
            await s.turn_on()

            await s.update()
            self.assertTrue(s.state)

    async def test_turn_off(self):
        """Test turn off the switch."""
        s = self.switch

        with patch.object(self.api, TEST_API_READ_DATA,
                          return_value=SWITCH_RETURN_ON):
            await s.turn_on()

            await s.update()
            self.assertTrue(s.state)

        await s.turn_off()

        await s.update()
        self.assertFalse(s.state)
