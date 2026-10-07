from __future__ import annotations

import httpx
from typing import Any


class DexScreenerAPI:
    """Real-time DEX token data from DexScreener API."""

    BASE_URL = "https://api.dexscreener.com/latest/dex"

    @classmethod
    async def fetch_token(cls, chain: str, pair_id: str) -> dict[str, Any] | None:
        """Fetch a single token pair from DexScreener."""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{cls.BASE_URL}/pairs/{chain}/{pair_id}",
                    timeout=10.0,
                )
                if response.status_code == 200:
                    return response.json()
            except (httpx.RequestError, httpx.TimeoutException):
                pass
        return None

    @classmethod
    async def search_tokens(cls, query: str) -> list[dict[str, Any]]:
        """Search for tokens by symbol or name."""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{cls.BASE_URL}/search",
                    params={"q": query},
                    timeout=10.0,
                )
                if response.status_code == 200:
                    data = response.json()
                    return data.get("pairs", [])
            except (httpx.RequestError, httpx.TimeoutException):
                pass
        return []


class CoinGeckoAPI:
    """Historical and market data from CoinGecko API (free tier)."""

    BASE_URL = "https://api.coingecko.com/api/v3"

    @classmethod
    async def fetch_market_data(cls, coin_id: str) -> dict[str, Any] | None:
        """Fetch market data for a coin."""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{cls.BASE_URL}/simple/price",
                    params={
                        "ids": coin_id,
                        "vs_currencies": "usd",
                        "include_market_cap": "true",
                        "include_24hr_vol": "true",
                        "include_24hr_change": "true",
                    },
                    timeout=10.0,
                )
                if response.status_code == 200:
                    return response.json()
            except (httpx.RequestError, httpx.TimeoutException):
                pass
        return None

    @classmethod
    async def trending_tokens(cls) -> list[dict[str, Any]]:
        """Fetch trending tokens."""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{cls.BASE_URL}/search/trending",
                    timeout=10.0,
                )
                if response.status_code == 200:
                    data = response.json()
                    return data.get("coins", [])
            except (httpx.RequestError, httpx.TimeoutException):
                pass
        return []
