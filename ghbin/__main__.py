# /bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2020 Aljosha Friemann <a.friemann@automate.wtf>
#
# Distributed under terms of the 3-clause BSD license.

from ghbin.cli import main

# pylint: disable=unexpected-keyword-arg
main(auto_envvar_prefix='GHBIN')
