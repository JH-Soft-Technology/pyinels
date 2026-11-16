"""Unit testing of iNels heat control library."""
from pyinels.const import (
    ATTR_THERM,
    HEAT_LEVEL_ATTENUATION,
    HEAT_LEVEL_COMFORT,
    HEAT_LEVEL_MINIMUM,
    HEAT_LEVEL_NORMAL
)

from tests.const_test import (
    TEST_API_CLASS_NAMESPACE,
    TEST_API_ROOM_DEVICES,
    TEST_API_READ_DATA,
    TEST_HOST,
    TEST_PORT,
    TEST_RAW_HEAT_CONTROL,
    TEST_VERSION
)

from pyinels.api import Api
from pyinels.device.pyTherm import pyTherm

from unittest.mock import patch
from unittest import TestCase

THERM_ID = "Pokoj_dole_Temperature"
THERM_NAME = "Pokoj"

THERM_VALUES = {
    "Pokoj_dole_Temperature": 22.75,
    "Pokoj_dole_StateTH": 21.0,
    "Pokoj_dole_StateM": 0,
    "Pokoj_dole_StateU": 1,
    "Pokoj_dole_StateN": 0,
    "Pokoj_dole_StateK": 0,
}

THERM_VALUES_WITHOUT_LEVELS = {
    "Pokoj_dole_Temperature": 22.75,
    "Pokoj_dole_StateTH": 21.0,
}


def read_values(values):
    """Simulate reading of the variables. Unknown variable raises error."""
    def read(ids):
        missing = [i for i in ids if i not in values]
        if missing:
            raise Exception(f"<Fault 8002: 'error'> {missing}")
        return {i: values[i] for i in ids}
    return read


class PyThermTest(TestCase):
    """Class to test iNels heat control library."""

    def setUp(self):
        """Setup all necesary instances and mocks."""
        self.patches = [
            patch(f'{TEST_API_CLASS_NAMESPACE}.ping', return_value=True),
            patch(f'{TEST_API_CLASS_NAMESPACE}.{TEST_API_ROOM_DEVICES}',
                  return_value=TEST_RAW_HEAT_CONTROL),
            patch(f'{TEST_API_CLASS_NAMESPACE}.{TEST_API_READ_DATA}',
                  side_effect=read_values(THERM_VALUES)),
        ]

        for p in self.patches:
            p.start()

        self.write = patch(
            f'{TEST_API_CLASS_NAMESPACE}._Api__writeValues',
            return_value=None).start()

        self.api = Api(TEST_HOST, TEST_PORT, TEST_VERSION)
        therms = [device for device in self.api.getRoomDevices(
            'Prizemi') if device.type == ATTR_THERM]

        self.therm = pyTherm(therms[0])

    def tearDown(self):
        """Destroy all instances and mocks."""
        self.api = None
        self.therm = None
        patch.stopall()
        self.patches = None

    def test_unique_id_and_name_presented(self):
        """Test when the unique id is presented."""
        t = self.therm

        self.assertEqual(t.unique_id, THERM_ID)
        self.assertEqual(t.name, THERM_NAME)

    def test_temperatures(self):
        """Test the current temperature and the set point."""
        t = self.therm

        self.assertEqual(t.current_temperature, 22.75)
        self.assertEqual(t.target_temperature, 21.0)

    def test_levels(self):
        """Test the supported and the active level."""
        t = self.therm

        self.assertEqual(t.levels, [HEAT_LEVEL_MINIMUM,
                                    HEAT_LEVEL_ATTENUATION,
                                    HEAT_LEVEL_NORMAL,
                                    HEAT_LEVEL_COMFORT])
        self.assertEqual(t.level, HEAT_LEVEL_ATTENUATION)

    def test_set_level(self):
        """Test selecting of the level writes the select variable."""
        t = self.therm

        t.set_level(HEAT_LEVEL_COMFORT)

        self.write.assert_called_once_with({"Pokoj_dole_VK": "1"})
        # read values are kept after the write
        self.assertEqual(t.current_temperature, 22.75)

    def test_set_unknown_level(self):
        """Test the unknown level raises an error."""
        with self.assertRaises(ValueError):
            self.therm.set_level("party")

        self.write.assert_not_called()

    def test_fetch_all_devices(self):
        """Test fetching of all devices reads set point and levels."""
        self.api.set_devices([self.therm._device])

        with patch.object(self.api, TEST_API_READ_DATA,
                          side_effect=read_values({
                              **THERM_VALUES,
                              "Pokoj_dole_StateU": 0,
                              "Pokoj_dole_StateN": 1,
                              "Pokoj_dole_StateTH": 22.5})):
            self.api.fetch_all_devices()

        self.assertEqual(self.therm.target_temperature, 22.5)
        self.assertEqual(self.therm.level, HEAT_LEVEL_NORMAL)

    def test_levels_not_exported(self):
        """Test heat control without exported levels still works."""
        with patch.object(self.api, TEST_API_READ_DATA,
                          side_effect=read_values(
                              THERM_VALUES_WITHOUT_LEVELS)):
            therms = [device for device in self.api.getRoomDevices(
                'Prizemi') if device.type == ATTR_THERM]
            t = pyTherm(therms[0])

            self.assertEqual(t.current_temperature, 22.75)
            self.assertEqual(t.target_temperature, 21.0)
            self.assertEqual(t.levels, [])
            self.assertIsNone(t.level)

            with self.assertRaises(ValueError):
                t.set_level(HEAT_LEVEL_COMFORT)
