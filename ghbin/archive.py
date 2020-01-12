# /bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2020 Aljosha Friemann <a.friemann@automate.wtf>
#
# Distributed under terms of the 3-clause BSD license.


import logging
import tarfile

LOGGER = logging.getLogger(__name__)


def extract(archive, directory, members):
    LOGGER.debug("extracting %s from %s to %s", members, archive, directory)

    with tarfile.open(archive, 'r:gz') as obj:
        for member in members:
            obj.extract(member, directory)

            yield member
