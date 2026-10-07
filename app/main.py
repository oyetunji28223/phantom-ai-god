from __future__ import annotations

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.config import settings
from app.core.safety import RiskGuard
from app.core.market_scanner import MarketScanner
from app.services.storage import TradeStore
from app.strategies.momentum import MomentumStrategy

app = FastAPI(title="Phantom AI God", version="0.1.0")
scanner = MarketScanner()
strategy = MomentumStrategy(minimum_score=65.0)
risk_guard = RiskGuard(
    max_trade_usd=settings.max_trade_usd,
    max_daily_loss_usd=settings.max_daily_loss_usd,
    max_drawdown_pct=settings.max_drawdown_pct,
)
trade_store = TradeStore()


@app.get("/health")
def health() -> dict:
    return {
        "status": "ok",
        "app": settings.app_name,
        "environment": settings.environment,
        "live_trading_enabled": settings.enable_live_trading,
        "emergency_shutdown": settings.emergency_shutdown,
    }


@app.get("/signals")
def fetch_signals() -> dict:
    raw_signals = scanner.scan()
    ranked = strategy.rank(raw_signals)
    return {
        "signals": [
            {
                "symbol": signal.symbol,
                "score": signal.score,
                "action": signal.action,
                "price_usd": signal.price_usd,
                "liquidity_usd": signal.liquidity_usd,
                "volume_24h": signal.volume_24h,
                "price_change_pct": signal.price_change_pct,
                "volatility": signal.volatility,
            }
            for signal in ranked
        ]
    }


@app.get("/trade-history")
def trade_history(limit: int = 10) -> dict:
    return {"trades": trade_store.get_recent_trades(limit=max(1, min(limit, 50)))}


@app.post("/evaluate-trade")
def evaluate_trade(trade: dict) -> dict:
    trade_value_usd = float(trade.get("trade_value_usd", 0.0))
    daily_loss_usd = float(trade.get("daily_loss_usd", 0.0))
    drawdown_pct = float(trade.get("drawdown_pct", 0.0))

    review = risk_guard.evaluate_trade(trade_value_usd, daily_loss_usd, drawdown_pct)
    return {
        "allowed": review.allowed,
        "reason": review.reason,
        "max_trade_usd": review.max_trade_usd,
    }


@app.post("/paper-trade")
def paper_trade() -> dict:
    if settings.enable_live_trading:
        return JSONResponse(status_code=400, content={"message": "Live trading is disabled in this environment."})

    top_signals = scanner.scan()[:3]
    orders = []
    for signal in top_signals:
        order = {
            "symbol": signal.symbol,
            "action": signal.action,
            "confidence": round(signal.score / 100, 2),
            "score": signal.score,
        }
        trade_store.log_trade(signal.symbol, signal.action, order["confidence"], signal.score)
        orders.append(order)

    return {
        "mode": "paper_trading",
        "orders": orders,
    }
