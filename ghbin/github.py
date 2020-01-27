# /bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2020 Aljosha Friemann <a.friemann@automate.wtf>
#
# Distributed under terms of the 3-clause BSD license.

import logging

import requests
from simple_tools.interaction import collect

from github import Github
from github.GithubException import RateLimitExceededException

LOGGER = logging.getLogger(__name__)


def download(repository, version, asset, client=None):
    try:
        client = (client if client is not None else Github()).get_repo(repository)

        release = client.get_latest_release() if version == 'latest' else client.get_release(version)
        assets = list(release.get_assets())

        asset = collect(asset.name for entry in release.get_assets()) if asset is None else asset
        asset_info = next((entry for entry in assets if entry.name == asset), None)

        if asset_info is None:
            raise RuntimeError(f"Could not find asset {asset} for {repository}: {list(asset.name for asset in assets)}")

        response = requests.get(asset_info.browser_download_url)

        if not response.ok:
            raise RuntimeError(f"failed to download {response.url}: {response.status_code}")

        return response.content
    except RateLimitExceededException:
        raise RuntimeError("Reached GitHub API limit (https://developer.github.com/v3/#rate-limiting).")
