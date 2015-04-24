#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Humbly cloned from captn3m0's HackerTray package. What a wonderful app he wrote."""

from setuptools import setup
from setuptools import find_packages

setup(name='argumanorg_indicator,',
      version='2.0.0',
      description='Arguman.org most recent argument indicator.',
      long_description='This indicator fetches most recently updated threads from Argument.org. It also includes the Gtk StatusIcon fallback from HackerTray in case AppIndicator is not available.',
      keywords='arguman system tray indicator unity',
      url='http://arguman.org/',
      author='Umut Karcı',
      author_email='umutkarci@std.sehir.edu.tr',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'requests>=2.5.3',
          'appdirs>=1.3.0',
      ],
      entry_points={
          'console_scripts': ['argumanorg_indicator=argumanorg_indicator:main'],
          },
      zip_safe=False)