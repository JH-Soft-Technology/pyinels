[![Board Status](https://dev.azure.com/JH-Soft-Technology/56876c97-c932-49e4-9f94-ee53648b47f2/46ab7c1c-c809-440e-a908-a8bf4905312d/_apis/work/boardbadge/f600c878-c9b8-49eb-8b68-79918bbf1841?columnOptions=1)](https://dev.azure.com/JH-Soft-Technology/56876c97-c932-49e4-9f94-ee53648b47f2/_boards/board/t/46ab7c1c-c809-440e-a908-a8bf4905312d/Microsoft.RequirementCategory/)
[![Build status](https://dev.azure.com/JH-Soft-Technology/pyinels/_apis/build/status/Pyinels)](https://dev.azure.com/JH-Soft-Technology/pyinels/_build/latest?definitionId=6)

PyInels
========
A Python library that handles communication with proprietary home intelligent system
named [iNels](https://www.inels.com/) by ElkoEP company.

This package is developed against iNels BUS version. It is not tested on older
version CU2 and does not support RF components.

Requirements
============
For smooth using you need to have Python 3.8 or higher.

Install
=======
Use PyPI repository
```
pip install pyinels
```

Usage
=====
See the test directory for examples.

Heat control
------------
Heat controls (`heat-control` in the Connection Server) are loaded as `therm`
devices. Wrap them with `pyTherm` to get the room temperature, the set point
and the active level:

```python
from pyinels.api import Api
from pyinels.device.pyTherm import pyTherm

api = Api("http://192.168.1.10", "8001", "CU3")
therms = [pyTherm(d) for d in api.getAllDevices() if d.type == "therm"]
api.fetch_all_devices()

for t in therms:
    print(t.name, t.current_temperature, t.target_temperature, t.level)

therms[0].set_level("comfort")  # minimum / attenuation / normal / comfort
```

The set point is computed by the central unit from the active level, so it
can not be written directly. Levels are available when the heat control
variables `<room>_StateM/U/N/K` and `<room>_VM/U/N/K` are exported from IDM
(`<room>` is the set point variable without the `_StateTH` suffix).
Without them only the temperatures are read.

Testing
=======
I use [tox](https://tox.readthedocs.io) for testing.

```
$ pip install tox

```

Reason
======
I wrote PyInels library to use it for [home assistant](https://www.home-assistant.io/) integration.

Watch Feature
=============
In the future I would like to rewrite the library with better efficiency such ass [Asyncio](https://blog.heroku.com/python37-dataclasses-async-await#asyncio-and-the-code-async-code-code-await-code-keywords).

[![buy me a coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/jhoralek)
