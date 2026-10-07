from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class SignalScore:
    symbol: str
    score: float
    action: str
    reason: str
    confidence: float


class AISignalScorer:
    def __init__(self, model_name: str = "stub-ai-v1") -> None:
        self.model_name = model_name

    def score(self, payload: dict[str, Any]) -> SignalScore:
        symbol = str(payload.get("symbol", "UNKNOWN"))
        price_change = float(payload.get("price_change_pct", 0.0))
        volume = float(payload.get("volume_24h", 0.0))
        liquidity = float(payload.get("liquidity_usd", 0.0))
        volatility = float(payload.get("volatility", 0.0))

        momentum_component = min(max(price_change * 3.0, 0.0), 60.0)
        volume_component = min(volume / 2_000_000 * 30.0, 30.0)
        liquidity_component = min(liquidity / 1_000_000 * 20.0, 20.0)
        volatility_component = min(volatility * 15.0, 15.0)

        score = round(momentum_component + volume_component + liquidity_component + volatility_component, 2)
        action = "buy" if score >= 65 else "hold"
        if score < 30:
            action = "hold"

        reason = (
            "strong momentum and liquidity profile" if action == "buy"
            else "insufficient signal strength for live action"
        )
        confidence = round(min(max(score / 100.0, 0.0), 1.0), 2)

        return SignalScore(
            symbol=symbol,
            score=score,
            action=action,
            reason=reason,
            confidence=confidence,
        )
