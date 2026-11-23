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


def test_risk_guard_rejects_negative_and_non_finite_inputs() -> None:
    guard = RiskGuard(max_trade_usd=250.0, max_daily_loss_usd=500.0, max_drawdown_pct=0.15)
    assert guard.evaluate_trade(-1.0, 0.0, 0.0).allowed is False
    assert guard.evaluate_trade(float("nan"), 0.0, 0.0).allowed is False


def test_risk_guard_respects_emergency_shutdown() -> None:
    guard = RiskGuard(250.0, 500.0, 0.15, emergency_shutdown=True)
    result = guard.evaluate_trade(10.0, 0.0, 0.0)
    assert result.allowed is False
    assert "shutdown" in result.reason
