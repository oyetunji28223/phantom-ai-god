from __future__ import annotations

from app.config import settings
from app.core.market_scanner import MarketScanner
from app.services.ai_pipeline import AIPipeline
from app.services.storage import TradeStore
from app.strategies.momentum import MomentumStrategy

scanner = MarketScanner()
strategy = MomentumStrategy(minimum_score=65.0)
trade_store = TradeStore()
ai_pipeline = AIPipeline()


def score_live_signal(payload: dict) -> dict:
    return ai_pipeline.run(payload)


def ranked_market_signals() -> list[dict]:
    signals = []
    for signal in scanner.scan():
        ranked = ai_pipeline.run(
            {
                "symbol": signal.symbol,
                "price_change_pct": signal.price_change_pct,
                "volume_24h": signal.volume_24h,
                "liquidity_usd": signal.liquidity_usd,
                "volatility": signal.volatility,
            }
        )
        signals.append({
            "symbol": ranked["symbol"],
            "score": ranked["score"],
            "action": ranked["action"],
            "confidence": ranked["confidence"],
            "reason": ranked["reason"],
            "market_signal": {
                "price_change_pct": signal.price_change_pct,
                "volume_24h": signal.volume_24h,
                "liquidity_usd": signal.liquidity_usd,
                "volatility": signal.volatility,
            },
        })
    return sorted(signals, key=lambda item: item["score"], reverse=True)


def create_demo_strategy_response() -> dict:
    return {
        "app": settings.app_name,
        "status": "live_demo_mode",
        "signals": ranked_market_signals()[:3],
        "recorded_trades": len(trade_store.get_recent_trades(limit=20)),
    }
