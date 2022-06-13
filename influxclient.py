#!/usr/bin/env python3
import logging
import os
import aiohttp

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
        self.session.headers.update({"Authorization": f"Token {token}",
                                     "Content-Type": "application/json"})

    async def __aenter__(self):
        return self

    async def __aexit__(self, *excinfo):
        if self.session:
            await self.session.close()
