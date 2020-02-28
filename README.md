[![Board Status](https://dev.azure.com/jhoralek/304a2e2f-7696-467f-b538-4ec92723bcee/28f199f2-c5a0-4a4b-a400-85861984b539/_apis/work/boardbadge/91e0de8b-0bbe-45b8-aaca-fc53ebf1125d)](https://dev.azure.com/jhoralek/304a2e2f-7696-467f-b538-4ec92723bcee/_boards/board/t/28f199f2-c5a0-4a4b-a400-85861984b539/Microsoft.RequirementCategory)
PyInels
========
A Python library that handles communication with proprietary home intelligent system
named [iNels](https://www.inels.com/) by ElkoEP company.

This package is developed against iNels BUS CU3 version. It is not tested on older
version CU2 and does not support RF components.

Requirements
============
For smooth using you need to have Python 3.7 or higher.

Install
=======
Use PyPI repository
```
pip install pyinels
```

Usage
=====
See the test directory for examples.

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
