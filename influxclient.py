#!/usr/bin/env python3
import asyncio
import logging
import os
import aiohttp

from typing import Any, Dict, List

# InfluxDB2 defaults

DEFAULT_ORG = "default"
DEFAULT_URL = "http://localhost:8086"


class InfluxClient:
    def __init__(
        self,
        token: str = os.getenv("INFLUXDB_TOKEN") or "",
        url: str = os.getenv("INFLUXDB_URL") or DEFAULT_URL,
        org: str = os.getenv("INFLUXDB_ORG") or DEFAULT_ORG,
        debug: bool = bool(os.getenv("DEBUG")) or False,
    ) -> None:
        assert token, "INFLUXDB_TOKEN or token param must be set"
        loglevel = logging.WARNING
        self.debug = debug
        if self.debug:
            loglevel = logging.DEBUG
        logging.basicConfig(
            format="%(asctime)s %(levelname)s:%(message)s", level=loglevel
        )
        self.log = logging.getLogger(__name__)
        self.log.debug("Logging established.")
        self.org = org
        self.api_url = url + "/api/v2"
        self.params = {"org": self.org}
        self.session = aiohttp.ClientSession()
        self.session.headers.update(
            {
                "Authorization": f"Token {token}",
                "Content-Type": "application/json",
            }
        )

    async def __aenter__(self):
        return self

    async def __aexit__(self, *excinfo):
        if self.session:
            await self.session.close()

    async def get(
        self,
        url: str,
        params: Dict[str, str] = {},
        use_session_params: bool = True,
    ) -> Dict[str, Any]:
        if use_session_params:
            params.update(self.params)
        self.log.debug(f"HTTP GET -> {url}, params=[{params}]")
        resp = await self.session.get(url, params=params)
        obj = await resp.json()
        self.log.debug(f"HTTP GET Response -> {obj}")
        return obj

    async def post(
        self,
        url: str,
        payloads: List[Dict[str, Any]],
        params: Dict[str, str] = {},
        use_session_params: bool = True,
    ) -> List[Any]:
        params = self.params
        if not use_session_params:
            params = {}
        if not payloads:
            return []
        self.log.debug(
            f"HTTP POST -> {url}, params=[{params}], "
            + f"first body = {payloads[0]}"
        )
        payload_futs = [
            self.session.post(url, json=x, params=params) for x in payloads
        ]
        resps = await asyncio.gather(*payload_futs)
        self.log.debug(f"HTTP POST Responses -> {resps}")
        return resps

    async def list_all(
        self, url: str, itemtype: str, pagesize: int = 20
    ) -> List[Dict[str, Any]]:
        """List all objects of a particular type."""
        o_list = []
        params: Dict[str, Any] = {"limit": pagesize}
        last_id = ""
        while True:
            if last_id:
                params.update({"after": last_id})
            obj = await self.get(url, params)
            if not obj:
                break
            i_list = obj[itemtype]
            if not i_list:
                break
            o_list.extend(i_list)
            last_id = i_list[-1]["id"]
        return o_list

    async def list_all_with_offset(
        self, url: str, itemtype: str, pagesize: int = 20
    )-> List[Dict[str,Any]]:
        """List all objects of a particular type."""
        o_list = []
        params: Dict[str, Any] = {"limit": pagesize}
        offset = 0
        while True:
            params.update({"offset": offset})
            obj = await self.get(url, params)
            if not obj:
                break
            i_list = obj[itemtype]
            if not i_list:
                break
            o_list.extend(i_list)
            offset += len(i_list)
        return o_list
