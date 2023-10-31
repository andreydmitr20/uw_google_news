import asyncio
import aiohttp
from .config import config
from .log import log, d


async def api_get(url, params=None):
    async with aiohttp.ClientSession() as api_session:
        async with api_session.get(url, params=params) as response:
            if "application/json" in response.headers.get("Content-Type", ""):
                return await response.json()
            else:
                # Handle unexpected Content-Type
                raise ValueError(
                    # f"Unexpected Content-Type: {response.headers.get('Content-Type')}"
                    f"Unexpected Content-Type: {response}"
                )


async def api_put(url, params=None, data=None):
    async with aiohttp.ClientSession() as api_session:
        async with api_session.put(url, params=params, data=data) as response:
            if "application/json" in response.headers.get("Content-Type", ""):
                return await response.json()
            else:
                # Handle unexpected Content-Type
                raise ValueError(
                    # f"Unexpected Content-Type: {response.headers.get('Content-Type')}"
                    f"Unexpected Content-Type: {response}"
                )


async def api_post(url, params=None, data=None):
    async with aiohttp.ClientSession() as api_session:
        async with api_session.post(url, params=params, data=data) as response:
            if "application/json" in response.headers.get("Content-Type", ""):
                return await response.json()
            else:
                # Handle unexpected Content-Type
                raise ValueError(
                    # f"Unexpected Content-Type: {response.headers.get('Content-Type')}"
                    f"Unexpected Content-Type: {response}"
                )


async def api_delete(url, params=None, data=None):
    async with aiohttp.ClientSession() as api_session:
        async with api_session.delete(url, params=params, data=data) as response:
            if "application/json" in response.headers.get("Content-Type", ""):
                return await response.json()
            else:
                # Handle unexpected Content-Type
                raise ValueError(
                    # f"Unexpected Content-Type: {response.headers.get('Content-Type')}"
                    f"Unexpected Content-Type: {response}"
                )
