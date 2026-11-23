from __future__ import annotations

from dataclasses import replace

from fastapi.testclient import TestClient

from app import main as main_module
from app.core.safety import RiskGuard
from app.main import app

client = TestClient(app)


def test_health_endpoint() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["app"] == "phantom-ai-god"


def test_root_dashboard_renders() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert "Phantom AI God" in response.text


def test_strategies_endpoint() -> None:
    response = client.get("/strategies")
    assert response.status_code == 200
    payload = response.json()
    assert "available" in payload
    assert isinstance(payload["available"], list)
    assert payload["available"]


def test_signals_endpoint() -> None:
    response = client.get("/signals")
    assert response.status_code == 200
    payload = response.json()
    assert "signals" in payload
    assert isinstance(payload["signals"], list)
    assert len(payload["signals"]) >= 1
    assert payload["signals"][0]["symbol"]


def test_signal_aggregate_endpoint() -> None:
    response = client.get("/signal-aggregate")
    assert response.status_code == 200
    payload = response.json()
    assert "signals" in payload
    assert isinstance(payload["signals"], list)


def test_evaluate_trade_endpoint_rejects_large_trade() -> None:
    response = client.post(
        "/evaluate-trade",
        json={"trade_value_usd": 500.0, "daily_loss_usd": 50.0, "drawdown_pct": 0.08},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["allowed"] is False


def test_paper_trade_endpoint() -> None:
    response = client.post("/paper-trade")
    assert response.status_code == 200
    payload = response.json()
    assert payload["mode"] == "paper_trading"
    assert "orders" in payload
    assert isinstance(payload["orders"], list)
    assert len(payload["orders"]) >= 1


def test_trade_history_endpoint() -> None:
    client.post("/paper-trade")
    response = client.get("/trade-history")
    assert response.status_code == 200
    payload = response.json()
    assert "trades" in payload
    assert isinstance(payload["trades"], list)


def test_evaluate_trade_rejects_non_numeric_payload() -> None:
    response = client.post("/evaluate-trade", json={"trade_value_usd": "abc"})
    assert response.status_code == 422


def test_evaluate_trade_rejects_negative_payload() -> None:
    response = client.post("/evaluate-trade", json={"trade_value_usd": -5})
    assert response.status_code == 422


def test_emergency_shutdown_blocks_paper_trade(monkeypatch) -> None:
    monkeypatch.setattr(
        main_module, "settings",
        replace(main_module.settings, emergency_shutdown=True),
    )
    response = client.post("/paper-trade")
    assert response.status_code == 403
    assert "emergency shutdown" in response.json()["message"].lower()


def test_emergency_shutdown_rejects_risk_evaluation(monkeypatch) -> None:
    monkeypatch.setattr(main_module, "risk_guard", RiskGuard(250, 500, 0.15, True))
    response = client.post("/evaluate-trade", json={"trade_value_usd": 10})
    assert response.status_code == 200
    assert response.json()["allowed"] is False


def test_trending_skips_malformed_upstream_items(monkeypatch) -> None:
    from app.services import market_api

    async def malformed_response():
        return [
            {"item": {"symbol": "x"}},
            {"unexpected": True},
            {"item": {"symbol": "ok", "name": "Okay"}},
        ]

    monkeypatch.setattr(
        market_api.CoinGeckoAPI,
        "trending_tokens",
        classmethod(lambda cls: malformed_response()),
    )
    response = client.get("/trending")
    assert response.status_code == 200
    assert {token["symbol"] for token in response.json()["tokens"]} == {"X", "OK"}
