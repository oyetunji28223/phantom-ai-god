from __future__ import annotations

from dataclasses import asdict, dataclass

from app.core.market_scanner import MarketScanner, TokenSignal


@dataclass(frozen=True)
class TradePlan:
    symbol: str
    action: str
    confidence: float
    score: float
    stop_loss_usd: float
    target_usd: float


class TradeEngine:
    def __init__(self, scanner: MarketScanner | None = None) -> None:
        self.scanner = scanner or MarketScanner()

    def build_plan(self, signal: TokenSignal) -> TradePlan:
        confidence = round(signal.score / 100, 2)
        stop_loss_usd = max(signal.price_usd * 0.9, 0.0)
        target_usd = signal.price_usd * (1 + max((signal.score / 100) * 0.25, 0.05))

        return TradePlan(
            symbol=signal.symbol,
            action=signal.action,
            confidence=confidence,
            score=signal.score,
            stop_loss_usd=stop_loss_usd,
            target_usd=target_usd,
        )

    def paper_trade_plan(self) -> list[dict]:
        plan_items = []
        for signal in self.scanner.scan()[:3]:
            trade = self.build_plan(signal)
            plan_items.append(asdict(trade))
        return plan_items
