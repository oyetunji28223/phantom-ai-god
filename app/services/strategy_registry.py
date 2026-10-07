from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class StrategyConfig:
    minimum_score: float = 65.0
    max_top_signals: int = 3
    enable_live_trading: bool = False


class StrategyRegistry:
    def __init__(self, config: StrategyConfig | None = None) -> None:
        self.config = config or StrategyConfig()

    def get_default(self) -> StrategyConfig:
        return self.config

    def list_available(self) -> list[str]:
        return ["momentum", "mean_reversion", "volume_breakout"]
