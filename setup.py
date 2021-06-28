# -*- coding: utf-8 -*-
"""
Created on Sat May  1 18:26:13 2021

@author: Amruta
"""
from setuptools import find_packages, setup

setup(
    name='TeachAid',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)