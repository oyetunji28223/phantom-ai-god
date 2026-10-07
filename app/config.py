from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    environment: str = "development"
    app_name: str = "phantom-ai-god"
    app_port: int = 8000
    max_trade_usd: float = 250.0
    max_daily_loss_usd: float = 500.0
    max_drawdown_pct: float = 0.15
    enable_live_trading: bool = False
    emergency_shutdown: bool = False
    log_level: str = "INFO"


def load_settings() -> Settings:
    return Settings(
        environment=os.getenv("ENVIRONMENT", "development"),
        app_name=os.getenv("APP_NAME", "phantom-ai-god"),
        app_port=int(os.getenv("APP_PORT", "8000")),
        max_trade_usd=float(os.getenv("MAX_TRADE_USD", "250.0")),
        max_daily_loss_usd=float(os.getenv("MAX_DAILY_LOSS_USD", "500.0")),
        max_drawdown_pct=float(os.getenv("MAX_DRAWDOWN_PCT", "0.15")),
        enable_live_trading=os.getenv("ENABLE_LIVE_TRADING", "false").lower() == "true",
        emergency_shutdown=os.getenv("EMERGENCY_SHUTDOWN", "false").lower() == "true",
        log_level=os.getenv("LOG_LEVEL", "INFO"),
    )


settings = load_settings()
