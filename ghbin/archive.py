# /bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2020 Aljosha Friemann <a.friemann@automate.wtf>
#
# Distributed under terms of the 3-clause BSD license.

import logging
import os
import tarfile
import zipfile

LOGGER = logging.getLogger(__name__)


def extract(archive, directory, members):
    LOGGER.debug("extracting %s from %s to %s", members, archive, directory)

    if '.tar' in archive:
        suffix = os.path.splitext(archive)[1]
        mode = f"r:{suffix.lstrip('.')}" if suffix != '.tar' else "r"

        LOGGER.debug("treating %s as tar with mode %s", archive, mode)

        with tarfile.open(archive, mode) as obj:
            for member in members:
                try:
                    obj.extract(member, directory)

                    yield member
                except KeyError as err:
                    raise RuntimeError(err, obj.namelist())
    elif archive.endswith('zip'):
        LOGGER.debug("treating %s as zip", archive)

        with zipfile.ZipFile(archive, 'r') as obj:
            for member in members:
                try:
                    obj.extract(member, directory)

                    yield member
                except KeyError as err:
                    raise RuntimeError(err, obj.namelist())
    else:
        raise NotImplementedError(f"extract function for filetype {archive}")
