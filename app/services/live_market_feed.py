from __future__ import annotations

from typing import Any

from app.services.market_api import CoinGeckoAPI, DexScreenerAPI


class LiveMarketFeed:
    """Real market data aggregator using public APIs."""

    def __init__(self) -> None:
        self.dex_api = DexScreenerAPI()
        self.cg_api = CoinGeckoAPI()

    async def fetch_trending(self) -> list[dict[str, Any]]:
        """Fetch trending tokens from CoinGecko, skipping malformed entries."""
        trending = await self.cg_api.trending_tokens()
        tokens: list[dict[str, Any]] = []
        for item in trending[:10]:
            details = item.get("item") if isinstance(item, dict) else None
            if not isinstance(details, dict):
                continue
            symbol = details.get("symbol")
            if not isinstance(symbol, str) or not symbol.strip():
                continue
            tokens.append(
                {
                    "symbol": symbol.upper(),
                    "name": details.get("name", symbol),
                    "market_cap_rank": details.get("market_cap_rank"),
                    "thumb": details.get("thumb"),
                }
            )
        return tokens

    async def fetch_coin_data(self, coin_id: str) -> dict[str, Any] | None:
        """Fetch detailed market data for a coin."""
        data = await self.cg_api.fetch_market_data(coin_id)
        if data and coin_id in data:
            coin_data = data[coin_id]
            return {
                "coin_id": coin_id,
                "price_usd": coin_data.get("usd", 0.0),
                "market_cap_usd": coin_data.get("usd_market_cap", 0.0),
                "volume_24h_usd": coin_data.get("usd_24h_vol", 0.0),
                "price_change_24h_pct": coin_data.get("usd_24h_change", 0.0),
            }
        return None
