from __future__ import annotations

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse

from app.config import settings
from app.core.market_scanner import MarketScanner
from app.core.safety import RiskGuard
from app.services.ai_pipeline import AIPipeline
from app.services.live_market_feed import LiveMarketFeed
from app.services.signal_aggregator import SignalAggregator
from app.services.storage import TradeStore
from app.services.strategy_registry import StrategyRegistry
from app.strategies.momentum import MomentumStrategy

app = FastAPI(title="Phantom AI God", version="0.2.0")
scanner = MarketScanner()
strategy = MomentumStrategy(minimum_score=65.0)
strategy_registry = StrategyRegistry()
signal_aggregator = SignalAggregator()
ai_pipeline = AIPipeline()
live_market_feed = LiveMarketFeed()
risk_guard = RiskGuard(
    max_trade_usd=settings.max_trade_usd,
    max_daily_loss_usd=settings.max_daily_loss_usd,
    max_drawdown_pct=settings.max_drawdown_pct,
)
trade_store = TradeStore()


@app.get("/", response_class=HTMLResponse)
def dashboard() -> str:
    return """
    <html>
      <head>
        <title>Phantom AI God</title>
        <style>
          body { font-family: Arial, sans-serif; background: #0b1020; color: #ecf2ff; margin: 0; padding: 32px; }
          .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 20px; }
          .card { background: #111a2f; border: 1px solid #24314d; border-radius: 12px; padding: 16px; box-shadow: 0 8px 18px rgba(0,0,0,0.2); }
          .badge { display: inline-block; background: #1c7c54; color: #fff; padding: 4px 8px; border-radius: 999px; font-size: 12px; }
          pre { background: #08111d; padding: 12px; border-radius: 8px; overflow: auto; max-height: 200px; }
          button { background: #3b82f6; color: white; border: none; border-radius: 8px; padding: 10px 14px; cursor: pointer; margin: 4px; }
          h3 { margin-top: 0; color: #58a3ff; }
        </style>
      </head>
      <body>
        <h1>Phantom AI God</h1>
        <div class="badge">AI Sniper Dashboard v0.2</div>
        <div style="margin-top: 20px;">
          <button onclick="loadDashboard()">Refresh</button>
          <button onclick="loadTrending()">Load Trending</button>
        </div>
        <div class="grid" style="margin-top: 20px;">
          <div class="card">
            <h3>System Health</h3>
            <div id="health">Loading...</div>
          </div>
          <div class="card">
            <h3>Strategy Registry</h3>
            <div id="strategies">Loading...</div>
          </div>
          <div class="card">
            <h3>AI Signals</h3>
            <pre id="signals">Loading...</pre>
          </div>
          <div class="card">
            <h3>Trending Tokens</h3>
            <pre id="trending">Loading...</pre>
          </div>
          <div class="card">
            <h3>Recent Trades</h3>
            <pre id="trades">Loading...</pre>
          </div>
        </div>
        <script>
          async function loadDashboard() {
            const health = await fetch('/health').then(r => r.json());
            const strategies = await fetch('/strategies').then(r => r.json());
            const signals = await fetch('/ai-signals').then(r => r.json());
            const trades = await fetch('/trade-history').then(r => r.json());
            document.getElementById('health').textContent = JSON.stringify(health, null, 2);
            document.getElementById('strategies').textContent = JSON.stringify(strategies, null, 2);
            document.getElementById('signals').textContent = JSON.stringify(signals.signals.slice(0, 3), null, 2);
            document.getElementById('trades').textContent = JSON.stringify(trades.trades.slice(0, 5), null, 2);
          }
          async function loadTrending() {
            const trending = await fetch('/trending').then(r => r.json());
            document.getElementById('trending').textContent = JSON.stringify(trending.tokens.slice(0, 5), null, 2);
          }
          loadDashboard();
        </script>
      </body>
    </html>
    """


@app.get("/health")
def health() -> dict:
    return {
        "status": "ok",
        "app": settings.app_name,
        "environment": settings.environment,
        "live_trading_enabled": settings.enable_live_trading,
        "emergency_shutdown": settings.emergency_shutdown,
        "version": "0.2.0",
    }


@app.get("/strategies")
def strategies() -> dict:
    config = strategy_registry.get_default()
    return {
        "available": strategy_registry.list_available(),
        "default": {
            "minimum_score": config.minimum_score,
            "max_top_signals": config.max_top_signals,
            "enable_live_trading": config.enable_live_trading,
        },
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


@app.get("/signal-aggregate")
def fetch_signal_aggregate() -> dict:
    return {"signals": signal_aggregator.aggregate()}


@app.get("/ai-signals")
def ai_signals() -> dict:
    aggregated = signal_aggregator.aggregate()
    scored = []
    for item in aggregated:
        scored.append(ai_pipeline.run(item))
    return {"signals": scored}


@app.get("/trending")
async def trending() -> dict:
    tokens = await live_market_feed.fetch_trending()
    return {"tokens": tokens}


@app.get("/market-data/{coin_id}")
async def market_data(coin_id: str) -> dict:
    data = await live_market_feed.fetch_coin_data(coin_id)
    if data:
        return {"data": data}
    return JSONResponse(status_code=404, content={"error": "coin not found"})


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
