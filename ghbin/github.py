# /bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2020 Aljosha Friemann <a.friemann@automate.wtf>
#
# Distributed under terms of the 3-clause BSD license.

import logging

import requests
from simple_tools.interaction import collect

LOGGER = logging.getLogger(__name__)


def download(repository, version, asset):
    release_info = requests.get(f"https://api.github.com/repos/{repository}/releases/{version}").json()

    if version == 'latest':
        version = release_info['name']

    if asset is None:
        asset = collect([entry['name'] for entry in release_info['assets']])

    return requests.get(f"https://github.com/{repository}/releases/download/{version}/{asset}")
