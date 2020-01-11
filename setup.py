# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    use_scm_version=True,
    include_package_data=True,
    entry_points={'console_scripts': [
        'ghbin=ghbin.cli:main']}
)
