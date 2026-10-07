from __future__ import annotations

from app.config import settings


def app_metadata() -> dict:
    return {
        "name": settings.app_name,
        "environment": settings.environment,
        "live_trading_enabled": settings.enable_live_trading,
        "emergency_shutdown": settings.emergency_shutdown,
    }
