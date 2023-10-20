#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: xingming
# Mail: huoxingming@gmail.com
# Created Time:  2015-12-11 01:25:34 AM
#############################################


from setuptools import setup, find_packages

setup(
    name = "fengmm521_blecam",
    version = "0.1.1",
    keywords = ("pathtool","timetool", "magetool", "mage"),
    description = "ble mouce and keyboard cam tool",
    long_description = "ble mouce and keyboard cam tool",
    license = "Apache License",

    url = "https://github.com/fengmm521/fengmm521_blecam",
    author = "mage",
    author_email = "mage@woodcol.com",

    packages = find_packages(),
    package_data={
        'fengmm521_blecam': ['_mac/*.so', '_windows/*.pyd'],
    },
    include_package_data = True,
    platforms = "any",
    install_requires = [],
    # install_requires = ['opencv-python>=4.7.0',
    #                     'pyserial',
    #                     'esptool',
    #                     'adafruit-ampy'],
    python_requires='>=3.9, <4'
)
