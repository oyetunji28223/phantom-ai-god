from __future__ import annotations

from app.core.market_scanner import TokenSignal


class MomentumStrategy:
    def __init__(self, minimum_score: float = 65.0):
        self.minimum_score = minimum_score

    def rank(self, signals: list[TokenSignal]) -> list[TokenSignal]:
        ranked = []
        for signal in signals:
            if signal.score >= self.minimum_score:
                ranked.append(signal)
        return sorted(ranked, key=lambda item: item.score, reverse=True)
