from __future__ import annotations

from typing import Any

from app.services.ai_scorer import AISignalScorer


class AIPipeline:
    def __init__(self, scorer: AISignalScorer | None = None) -> None:
        self.scorer = scorer or AISignalScorer()

    def run(self, payload: dict[str, Any]) -> dict[str, Any]:
        result = self.scorer.score(payload)
        return {
            "symbol": result.symbol,
            "score": result.score,
            "action": result.action,
            "reason": result.reason,
            "confidence": result.confidence,
            "model": self.scorer.model_name,
        }
