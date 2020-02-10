"""Setup script for pyinels package."""
from setuptools import setup, find_packages
from inels.const import NAME, VERSION


setup(name=NAME,
      version=VERSION,
      url='https://github.com/jhoralek/pyinels',
      license='MIT',
      author='Jiri horalek',
      author_email='horalek.jiri@gmail.com',
      description='Python library for iNels BUS CU3',
      long_description_content_type='text/markdown',
      charset='UTF-8',
      variant='GFM',
      long_description=open('README.md').read(),
      zip_safe=False,
      classifiers=[
          "License :: OSI Approved :: MIT License",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.7",
      ],
      packages=find_packages(),
      test_suite='unittest')
