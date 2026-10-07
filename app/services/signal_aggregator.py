from __future__ import annotations

from typing import Any

from app.services.market_feed import MarketFeedService


class SignalAggregator:
    def __init__(self, feed_service: MarketFeedService | None = None) -> None:
        self.feed_service = feed_service or MarketFeedService()

    def aggregate(self) -> list[dict[str, Any]]:
        snapshots = self.feed_service.fetch_market_feed()
        return [
            {
                "symbol": item.symbol,
                "price_usd": item.price_usd,
                "liquidity_usd": item.liquidity_usd,
                "volume_24h": item.volume_24h,
                "price_change_pct": item.price_change_pct,
                "volatility": item.volatility,
                "source": item.source,
            }
            for item in snapshots
        ]
