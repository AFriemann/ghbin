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
def root(ctx, debug, trace, config_path):
    coloredlogs.install(level=logging.DEBUG if debug else logging.INFO)

    if not trace:
        logging.getLogger("botocore").setLevel(logging.WARN)
        logging.getLogger("urllib3").setLevel(logging.WARN)
        logging.getLogger("github").setLevel(logging.WARN)

    ctx.obj = config.load(config_path)


@root.command('install')
@click.option("--token", help="GitHub access token.")
@click.option("--force", is_flag=True, default=False, help="GitHub access token.")
@click.pass_obj
def root_install(obj, token, force):
    client = github.Github(token)

    for source in obj.get('sources', []):
        name = source['name']
        repository = source['repository']

        asset = source.get('asset')
        version = source.get('version', 'latest')

        if not force and 'extract' not in source and files.exists(os.path.expanduser(f"~/.local/bin/{name}")):
            # bail early when it's a binary and already installed
            print(f"skipping {name} from {repository}, already installed")
            continue

        print(f"installing {name} from {repository}")

        content = github.download(repository, version, asset, client=client)

        with tempfile.TemporaryDirectory() as dirname:
            tmp_path = os.path.join(dirname, asset)

            with open(tmp_path, 'wb') as stream:
                stream.write(content)

            if 'extract' in source:
                for member in archive.extract(tmp_path, dirname, source['extract']):
                    files.install(os.path.join(dirname, member), os.path.expanduser(f"~/.local/bin/{member}"))
            else:
                files.install(tmp_path, os.path.expanduser(f"~/.local/bin/{name}"))


@root.command('update')
@click.pass_obj
def root_update(obj):
    for source in obj.get('sources', []):
        print(source)


@root.group('config')
def cfg():
    pass


@cfg.command('show')
@click.pass_obj
def cfg_show(obj):
    print(obj)


def main():
    try:
        root(auto_envvar_prefix='GHBIN') # pylint: disable=no-value-for-parameter,unexpected-keyword-arg
    except RuntimeError as err:
        print(err)
