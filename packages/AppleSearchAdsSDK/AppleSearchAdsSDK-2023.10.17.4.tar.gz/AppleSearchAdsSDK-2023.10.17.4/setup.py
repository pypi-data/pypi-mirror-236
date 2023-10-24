# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : setup
# Time       ：2023/9/17 08:11
# Author     ：leo.wang
# version    ：python 3.9
# Description：
"""
from setuptools import setup, find_packages

GFICLEE_VERSION = '2023.10.17.4'
setup(
    name='AppleSearchAdsSDK',
    version=GFICLEE_VERSION,
    packages=find_packages(),
    install_requires=[
        "requests",
        "pyjwt"
    ],
)
