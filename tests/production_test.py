"""Production test cases."""
import asyncio

from pyinels.api import Api
from pyinels.device.pyLight import pyLight
from pyinels.device.pySwitch import pySwitch
from pyinels.device.pyDoor import pyDoor
from pyinels.device.pyShutter import pyShutter

# from unittest import async_case

MMS_IP_ADDRESS = "192.168.2.102"
PLC_IP_ADDRESS = "192.168.2.101"


# class ProductionTest(async_case.IsolatedAsyncioTestCase):
class ProductionTest():
    """Library used agains production server."""

    def setUp(self):
        """Setup all necessary instances nad mocks."""
        self.api = Api(f'http://{MMS_IP_ADDRESS}', 8001, "CU3")

    async def asyncSetUp(self):
        """Setup all neccessary async stuff."""
        devices = await self.api.getAllDevices()
        self.api.set_devices(devices)

    def tearDown(self):
        """Remove all attached properties."""
        self.api = None

    async def test_ping_success(self):
        """Ping test."""
        ping = await self.api.ping()

        self.assertEqual(ping, True)

    async def test_plcIp_address(self):
        """Get Ip address of the PLC."""
        ip = await self.api.getPlcIp()

        self.assertEqual(PLC_IP_ADDRESS, ip)

    def test_loaded_devices(self):
        """Are devices from api loaded?"""
        self.assertGreater(len(self.api.devices), 0)

    async def test_create_light(self):
        """create and test light."""
        devices = [
            x for x in self.api.devices
            if x.id == "SV_7_Pokoj_dole"]

        light = await pyLight(devices[0])
        self.assertEqual(light.state, False)

        await light.turn_on()
        self.assertEqual(light.state, True)
        asyncio.sleep(4)
        await light.turn_off()
        self.assertEqual(light.state, False)
        asyncio.sleep(4)

        await light.set_brightness(50)
        self.assertEqual(light.state, True)
        asyncio.sleep(4)
        await light.set_brightness(100)
        self.assertEqual(light.state, True)
        asyncio.sleep(4)
        await light.set_brightness(0)
        self.assertEqual(light.state, False)

    async def test_create_switch(self):
        """create and test switch."""
        devices = [
            x for x in self.api.devices if x.id
            == "ZAS_1B_Pokoj_dole"]

        switch = await pySwitch(devices[0])

        await switch.turn_off()
        self.assertEqual(switch.state, False)
        asyncio.sleep(4)
        await switch.turn_on()
        self.assertEqual(switch.state, True)

    async def test_create_door(self):
        """crate and test door."""
        devices = [
            x for x in self.api.devices if x.id
            == "Vrata_Garaz"]

        door = await pyDoor(devices[0])

        await door.turn_on()
        asyncio.sleep(30)
        await door.turn_off()

    async def test_create_shutter(self):
        """create and test shutter."""
        devices = [
            x for x in self.api.devices
            if x.id == "ROL_Pokoj_host_nahoru_ROL_Pokoj_host_dolu"]

        shutter = await pyShutter(devices[0])

        await shutter.pull_up()
        asyncio.sleep(20)
        await shutter.stop()
        await shutter.pull_down()
        asyncio.sleep(10)
        await shutter.stop()
