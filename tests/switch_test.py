"""Unit testing of iNels switch library."""

from tests.const_test import (
    TEST_DATA_SWITCH,
    TEST_HOST,
    TEST_INELS_BUS3_NAMESPACE,
    TEST_PORT
)

from inels.cu3 import InelsBus3
from inels.device import (
    InelsDevice,
    DeviceType
)

from inels.device.InelsSwitch import InelsSwitch

from unittest.mock import patch
from unittest import TestCase


class InelsSwitchTest(TestCase):
    """Class to test iNels switch library."""

    def setUp(self):
        """Setup all necesary instances and mocks."""
        self.patches = [
            patch(f'{TEST_INELS_BUS3_NAMESPACE}.ping', return_value=True),
            patch(f'{TEST_INELS_BUS3_NAMESPACE}.read',
                  return_value={TEST_DATA_SWITCH['id']: 1}),
            patch('inels.device.InelsDevice._write', return_value=None)
        ]

        self.proxy = InelsBus3(TEST_HOST, TEST_PORT)
        self.device = InelsDevice(TEST_DATA_SWITCH['name'],
                                  TEST_DATA_SWITCH['id'],
                                  DeviceType.SWITCH, self.proxy)

        self.switch = InelsSwitch(self.device)
        # patching ping method in IneslBus3. It will be executed every test
        for p in self.patches:
            p.start()

    def tearDown(self):
        """Destroy all instances and mocks."""
        self.proxy = None
        self.device = None
        self.switch = None
        patch.stopall()

    def test_initialize_switch(self):
        """Initialize switch and test state."""
        self.assertEqual(TEST_DATA_SWITCH['id'], self.switch.device.id)

    def test_state_switch(self):
        """Test state of the switch."""
        state = self.switch.state
        self.assertEqual(state, True)

    def test_toggle_switch(self):
        """Toogle of the switch."""
        self.switch.toggle()
        self.assertEqual(self.switch.state, False)

        self.switch.toggle()
        self.assertEqual(self.switch.state, True)
