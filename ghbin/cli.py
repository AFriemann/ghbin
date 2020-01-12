# /bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2020 Aljosha Friemann <a.friemann@automate.wtf>
#
# Distributed under terms of the 3-clause BSD license.

import logging
import os
import tempfile

import click
import coloredlogs

import ghbin.archive as archive
import ghbin.config as config
import ghbin.files as files
import ghbin.github as github


@click.group()
@click.option("-d", "--debug", is_flag=True, default=False, show_default=True, help="Enable debug logging.")
@click.option("-t", "--trace", is_flag=True, default=False, show_default=True, help="Enable spammy logging.")
@click.option('-c', '--config', 'config_path', type=click.Path(exists=True, dir_okay=False),
              default=os.path.expanduser('~/.config/ghbin/config.yaml'))
@click.pass_context
def main(ctx, debug, trace, config_path):
    coloredlogs.install(level=logging.DEBUG if debug else logging.INFO)

    if not trace:
        logging.getLogger("botocore").setLevel(
            logging.WARN if not debug else logging.INFO)
        logging.getLogger("urllib3").setLevel(
            logging.WARN if not debug else logging.INFO)

    ctx.obj = config.load(config_path)


@main.command('install')
@click.pass_obj
def main_install(obj):
    for source in obj.get('sources', []):
        name = source['name']
        repository = source['repository']

        print(f"installing {name} from {repository}")

        asset = source.get('asset')
        version = source.get('version', 'latest')

        response = github.download(repository, version, asset)

        if response.ok:
            with tempfile.TemporaryDirectory() as dirname:
                tmp_path = os.path.join(dirname, asset)

                with open(tmp_path, 'wb') as stream:
                    stream.write(response.content)

                if 'extract' in source:
                    for member in archive.extract(tmp_path, dirname, source['extract']):
                        files.install(os.path.join(dirname, member), os.path.expanduser(f"~/.local/bin/{member}"))
                else:
                    files.install(tmp_path, os.path.expanduser(f"~/.local/bin/{name}"))


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
