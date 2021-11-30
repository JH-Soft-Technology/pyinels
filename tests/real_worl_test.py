"""Unit testing of iNels real library."""

from pyinels.api import Api
from unittest import TestCase

# from pyinels.const import ATTR_LIGHT, ATTR_SHUTTER
# from pyinels.device.pyLight import pyLight
# from pyinels.device.pyShutter import pyShutter


class PyRealTests(TestCase):
    """Class to test iNels real connection."""

    def setUp(self):
        self.api = Api("http://192.168.2.102", 8001, "CU3")

    def tearDown(self):
        """Destroy all instances."""
        self.api = None

    # def test_online(self):
    #     """Test in real world"""

    #     ping = self.api.ping()
    #     self.assertTrue(ping)

    #     devices = self.api.getAllDevices()
    #     self.assertGreater(len(devices), 0)

    #     lights = [device for device in devices if device.type == ATTR_LIGHT]
    #     self.assertGreater(len(lights), 0)

    #     light = pyLight(lights[6])
    #     self.assertEqual(light.name, "Pokoj")

    #     light.set_brightness(20)

    # def test_devices_data_fetch(self):
        # """Fetching all data from devices."""

        # devices = self.api.getAllDevices()
        # self.assertGreater(len(devices), 0)

        # persisted_devices = self.api.devices
        # self.assertGreater(len(persisted_devices), 0)

        # lights = [device for device in devices if device.type == ATTR_LIGHT]
        # self.assertGreater(len(lights), 0)
        # light = pyLight(lights[6])
        # self.assertEqual(light.name, "Pokoj")

        # light.set_brightness(20)

        # devs_values = self.api.read_all()
        # self.assertGreater(len(devs_values), 0)

        # l_value = light._device.get_value()
        # self.assertEqual(l_value[light.unique_id], 0)

    # def test_shutter_data_fetch(self):
    #     """Fetching shutter data from api."""

    #     devices = self.api.getAllDevices()
    #     self.assertGreater(len(devices), 0)

    #     shutters = [device for device in devices
    # if device.type == ATTR_SHUTTER]
    #     self.assertGreater(len(shutters), 0)

    #     shutter = pyShutter(shutters[0])
    #     self.assertEqual(shutter.name, "Zal OB")

    #     value = shutter._device.get_value()
    #     self.assertGreater(len(value), 0)
