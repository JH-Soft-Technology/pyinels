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
