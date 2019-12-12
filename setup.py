from setuptools import setup, find_packages
from pyinels3.const import NAME, VERSION

setup(name=NAME,
      version=VERSION,
      url='https://github.com/jhoralek/pyinels3',
      license='MIT',
      author='Jiri horalek',
      author_email='horalek.jiri@gmail.com',
      description='Python library for iNels BUS CU3',
      packages=find_packages(exclude=['tests']),
      long_description=open('README.md').read(),
      zip_safe=False,
      test_suite='unittest')
