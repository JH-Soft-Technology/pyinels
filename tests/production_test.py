"""Production test cases."""
from time import sleep

from pyinels.api import Api
from pyinels.device.pyLight import pyLight
from pyinels.device.pySwitch import pySwitch
from pyinels.device.pyDoor import pyDoor
from pyinels.device.pyShutter import pyShutter

# from unittest import TestCase

# class ProductionTest(TestCase):


class ProductionTest():
    """Library used agains production server."""

    def setUp(self):
        """Setup all necessary instances nad mocks."""
        self.api = Api("http://192.168.2.102", 8001, "CU3")
        self.devices = self.api.devices

    def tearDown(self):
        """Remove all attached properties."""
        self.api = None
        self.devices = None

    def test_ping_success(self):
        """Ping test."""
        ping = self.api.proxy.ping()

        self.assertEqual(ping, True)

    def test_loaded_devices(self):
        """Are devices from api loaded?"""
        self.assertGreater(len(self.devices), 0)

    def test_create_light(self):
        """create and test light."""
        devices = [
            x for x in self.devices
            if x.id == "SV_7_Pokoj_dole"]

        light = pyLight(devices[0])
        self.assertEqual(light.state, False)

        light.turn_on()
        self.assertEqual(light.state, True)
        sleep(4)
        light.turn_off()
        self.assertEqual(light.state, False)
        sleep(4)

        light.set_brightness(50)
        self.assertEqual(light.state, True)
        sleep(4)
        light.set_brightness(100)
        self.assertEqual(light.state, True)
        sleep(4)
        light.set_brightness(0)
        self.assertEqual(light.state, False)

    def test_create_switch(self):
        """create and test switch."""
        devices = [
            x for x in self.devices if x.id
            == "ZAS_1B_Pokoj_dole"]

        switch = pySwitch(devices[0])

        switch.turn_off()
        self.assertEqual(switch.state, False)
        sleep(4)
        switch.turn_on()
        self.assertEqual(switch.state, True)

    def test_create_door(self):
        """crate and test door."""
        devices = [
            x for x in self.devices if x.id
            == "Vrata_Garaz"]

        door = pyDoor(devices[0])

        door.turn_on()
        sleep(30)
        door.turn_off()

    def test_create_shutter(self):
        """create and test shutter."""
        devices = [
            x for x in self.devices
            if x.id == "ROL_Pokoj_host_nahoru_ROL_Pokoj_host_dolu"]

        shutter = pyShutter(devices[0])

        shutter.pull_up()
        sleep(20)
        shutter.stop()
        shutter.pull_down()
        sleep(10)
        shutter.stop()
