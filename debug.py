"""Debuging inels library."""
from inels.cu3 import InelsBus3

proxy = InelsBus3("http://185.75.136.145", "8001")

print(proxy.getRooms())

garage_devs = proxy.getRoomDevices('Garaz')

for garage in garage_devs:
    print(garage)
