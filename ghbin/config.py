# /bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2020 Aljosha Friemann <a.friemann@automate.wtf>
#
# Distributed under terms of the 3-clause BSD license.

from typing import Dict

import ruamel.yaml as yaml


def load(path: str) -> Dict:
    with open(path, 'rb') as stream:
        return yaml.safe_load(stream.read().decode())
