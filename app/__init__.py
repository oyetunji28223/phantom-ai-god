from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class TradeDecision:
    symbol: str
    action: Literal["buy", "sell", "hold"]
    confidence: float
    score: float
    reason: str
    max_trade_usd: float


@dataclass(frozen=True)
class MarketSnapshot:
    symbol: str
    price_usd: float
    liquidity_usd: float
    volume_24h: float
    price_change_pct: float
    volatility: float
