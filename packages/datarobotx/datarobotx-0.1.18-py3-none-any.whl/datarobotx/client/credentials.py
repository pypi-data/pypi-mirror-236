#
# Copyright 2023 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.

from __future__ import annotations

import logging
from typing import Any, cast, Dict, List

from datarobotx.common.client import raise_value_error, session

logger = logging.getLogger("drx")


async def get_credentials() -> List[Dict[str, Any]]:
    """List credentials available to the user"""
    url = "/credentials/"
    async with session.get(url, allow_redirects=False, params={"limit": 1000}) as resp:
        if resp.status != 200:
            await raise_value_error(resp)
        json = await resp.json()
        return cast(List[Dict[str, Any]], json["data"])
