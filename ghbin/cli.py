# /bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2020 Aljosha Friemann <a.friemann@automate.wtf>
#
# Distributed under terms of the 3-clause BSD license.

import json
import os
import shutil
import tempfile

import click
import requests
from simple_tools.interaction import collect

import ghbin.config as config


@click.group()
@click.option('-c', '--config', 'config_path', type=click.Path(exists=True, dir_okay=False),
              default=os.path.expanduser('~/.config/ghbin/config.yaml'))
@click.pass_context
def main(ctx, config_path):
    ctx.obj = config.load(config_path)


@main.command('install')
@click.pass_obj
def main_install(obj):
    for source in obj.get('sources', []):
        #print(source)

        name = source['name']
        asset = source.get('asset')
        version = source.get('version', 'latest')
        repository = source['repository']

        release_info = requests.get(f"https://api.github.com/repos/{repository}/releases/{version}").json()

        if version == 'latest':
            version = release_info['name']

        if asset is None:
            asset = collect([entry['name'] for entry in release_info['assets']])

        response = requests.get(f"https://github.com/{repository}/releases/download/{version}/{asset}")

        if response.ok:
            with tempfile.TemporaryDirectory() as dirname:
                tmp_path = os.path.join(dirname, asset)

                with open(tmp_path, 'wb') as stream:
                    stream.write(response.content)

                fpath = os.path.expanduser(f"~/.local/bin/{name}")

                print(f"installing {asset} to {fpath}")

                shutil.move(tmp_path, fpath)
                os.chmod(fpath, 0o755)


@main.command('update')
@click.pass_obj
def main_update(obj):
    for source in obj.get('sources', []):
        print(source)


@main.group('config')
def cfg():
    pass


@cfg.command('show')
@click.pass_obj
def cfg_show(obj):
    print(obj)
