from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class MarketFeedSnapshot:
    symbol: str
    price_usd: float
    liquidity_usd: float
    volume_24h: float
    price_change_pct: float
    volatility: float
    source: str = "stub"


class MarketFeedService:
    def __init__(self, source: str = "stub") -> None:
        self.source = source

    def fetch_snapshot(self) -> list[dict[str, Any]]:
        return [
            {
                "symbol": "DOGE",
                "price_usd": 0.18,
                "liquidity_usd": 820000,
                "volume_24h": 2_400_000,
                "price_change_pct": 12.4,
                "volatility": 0.72,
                "source": self.source,
            },
            {
                "symbol": "PEPE",
                "price_usd": 0.000018,
                "liquidity_usd": 630000,
                "volume_24h": 1_900_000,
                "price_change_pct": 9.7,
                "volatility": 0.81,
                "source": self.source,
            },
            {
                "symbol": "BONK",
                "price_usd": 0.000028,
                "liquidity_usd": 540000,
                "volume_24h": 1_100_000,
                "price_change_pct": 6.9,
                "volatility": 0.61,
                "source": self.source,
            },
        ]

    def fetch_market_feed(self) -> list[MarketFeedSnapshot]:
        return [
            MarketFeedSnapshot(
                symbol=item["symbol"],
                price_usd=item["price_usd"],
                liquidity_usd=item["liquidity_usd"],
                volume_24h=item["volume_24h"],
                price_change_pct=item["price_change_pct"],
                volatility=item["volatility"],
                source=item["source"],
            )
            for item in self.fetch_snapshot()
        ]
