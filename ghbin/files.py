# /bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2020 Aljosha Friemann <a.friemann@automate.wtf>
#
# Distributed under terms of the 3-clause BSD license.

import logging
import os
import shutil

LOGGER = logging.getLogger(__name__)


def install(source, target, mode=0o755):
    LOGGER.debug("installing %s to %s with mode %o", source, target, mode)

    shutil.move(source, target)
    os.chmod(target, mode)
