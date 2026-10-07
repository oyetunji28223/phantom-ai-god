from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RiskCheckResult:
    allowed: bool
    reason: str
    max_trade_usd: float


class RiskGuard:
    def __init__(self, max_trade_usd: float, max_daily_loss_usd: float, max_drawdown_pct: float):
        self.max_trade_usd = max_trade_usd
        self.max_daily_loss_usd = max_daily_loss_usd
        self.max_drawdown_pct = max_drawdown_pct

    def evaluate_trade(self, trade_value_usd: float, daily_loss_usd: float, drawdown_pct: float) -> RiskCheckResult:
        if trade_value_usd > self.max_trade_usd:
            return RiskCheckResult(False, "trade exceeds configured max trade size", self.max_trade_usd)

        if daily_loss_usd > self.max_daily_loss_usd:
            return RiskCheckResult(False, "daily loss exceedance reached", self.max_trade_usd)

        if drawdown_pct > self.max_drawdown_pct:
            return RiskCheckResult(False, "portfolio drawdown exceeds safety threshold", self.max_trade_usd)

        return RiskCheckResult(True, "risk checks passed", min(self.max_trade_usd, trade_value_usd))
