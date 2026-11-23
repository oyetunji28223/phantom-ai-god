# Phantom AI God

Phantom AI God is a paper-trading and signal-prototyping API starter.

**It is not a live trading system.** There is no wallet integration, key
handling, order signing, or exchange execution. `/signals`, `/ai-signals`,
`/signal-aggregate` and `/paper-trade` currently use demo/stub market data;
only `/trending` and `/market-data/{coin_id}` call public read-only market
APIs. The "AI" scorer is a deterministic weighted formula, not a trained model.

This repository is intentionally structured as a safe, testable foundation for:
- market scanning and signal generation
- risk controls and execution guardrails
- paper trading and simulation
- monitoring, alerts, and future AI scoring

## Architecture

```text
phantom-ai-god/
├── app/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── market_scanner.py
│   │   └── safety.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── ai_pipeline.py
│   │   ├── ai_scorer.py
│   │   ├── live_market_feed.py
│   │   ├── market_api.py
│   │   ├── market_feed.py
│   │   ├── signal_aggregator.py
│   │   ├── storage.py
│   │   ├── strategy_registry.py
│   │   └── trade_engine.py
│   ├── strategies/
│   │   ├── __init__.py
│   │   └── momentum.py
│   ├── config.py
│   ├── main.py
│   └── __init__.py
├── scripts/run_dev.py
├── tests/
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
├── scripts/
│   └── run_dev.py
└── .dockerignore
```

## Quick start

### Local Python

1. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell, use `.venv\Scripts\activate` instead.

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Configure environment variables

```bash
cp .env.example .env
```

4. Run the API

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

5. Open the API docs

- Swagger UI: http://localhost:8000/docs
- Health check: http://localhost:8000/health

### Docker

```bash
docker compose up --build
```

An `.env` file is no longer required; safe defaults are set in
`docker-compose.yml`. Override them in your shell or an untracked `.env` if you
need different risk limits.

Then open:
- http://localhost:8000/docs

## API overview

- GET /health
- GET /signals
- GET /signal-aggregate
- GET /ai-signals
- GET /trending
- GET /market-data/{coin_id}
- GET /strategies
- GET /trade-history
- POST /evaluate-trade
- POST /paper-trade

## Safety model

- max trade size cap
- max daily loss cap
- max drawdown cap
- negative / non-finite risk inputs are rejected with HTTP 422
- `EMERGENCY_SHUTDOWN=true` blocks both `/paper-trade` and `/evaluate-trade`
- no live execution path exists in this codebase (there is nothing to enable)

## Roadmap

- [x] read-only live market data adapter (DexScreener / CoinGecko)
- [x] SQLite paper-trade persistence
- [x] deterministic AI-style scoring stub
- [x] local HTML dashboard
- [ ] trained scoring model
- [ ] wallet and execution integration (not implemented by design)
- [ ] backtesting engine

## Disclaimer

This project is for research and simulation purposes. It should not be used for real trading without a strict testing and audit process.
