from __future__ import annotations

from app.core.safety import RiskGuard


def test_risk_guard_allows_safe_trade() -> None:
    guard = RiskGuard(max_trade_usd=250.0, max_daily_loss_usd=500.0, max_drawdown_pct=0.15)
    result = guard.evaluate_trade(100.0, 50.0, 0.08)
    assert result.allowed is True
    assert result.reason == "risk checks passed"


def test_risk_guard_rejects_large_trade() -> None:
    guard = RiskGuard(max_trade_usd=250.0, max_daily_loss_usd=500.0, max_drawdown_pct=0.15)
    result = guard.evaluate_trade(500.0, 50.0, 0.08)
    assert result.allowed is False
    assert "trade exceeds" in result.reason


def test_risk_guard_rejects_drawdown() -> None:
    guard = RiskGuard(max_trade_usd=250.0, max_daily_loss_usd=500.0, max_drawdown_pct=0.15)
    result = guard.evaluate_trade(100.0, 50.0, 0.2)
    assert result.allowed is False
    assert "drawdown" in result.reason
