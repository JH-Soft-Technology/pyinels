"""Unit testing of iNels real library."""

# from pyinels.const import ATTR_LIGHT

from pyinels.api import Api
# from pyinels.device.pyLight import pyLight

from unittest import TestCase


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

    #     devivces = self.api.getAllDevices()
    #     self.assertGreater(len(devivces), 0)

    #     lights = [device for device in devivces if device.type == ATTR_LIGHT]
    #     self.assertGreater(len(lights), 0)

    #     light = pyLight(lights[6])
    #     self.assertEqual(light.name, "Pokoj")

    #     light.set_brightness(20)
