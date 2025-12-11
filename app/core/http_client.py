#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :http_client.py
# @Time      :2025/12/11 13:40
# @Author    :Dongguadada

import httpx
from .config import get_http_client_config

class HttpClient:
    def __init__(self):
        config = get_http_client_config()
        self.client = httpx.AsyncClient(
            # limits=httpx.Limits(**config["http_max_connections"]),
            # http2=config["http2_enabled"]
        )

    async def get(self, url: str, **kwargs):
        response = await self.client.get(url, **kwargs)
        response.raise_for_status()
        return response

    async def post(self, url: str, **kwargs):
        response = await self.client.post(url, **kwargs)
        response.raise_for_status()
        return response

    async def close(self):
        await self.client.aclose()

http_client = HttpClient()