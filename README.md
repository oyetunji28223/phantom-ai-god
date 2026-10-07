# Phantom AI God

Phantom AI God is an AI-assisted memecoin sniper and execution system starter.

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
│   │   ├── market_feed.py
│   │   └── trade_engine.py
│   ├── strategies/
│   │   ├── __init__.py
│   │   └── momentum.py
│   ├── config.py
│   ├── main.py
│   └── __init__.py
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

Then open:
- http://localhost:8000/docs

## API overview

- GET /health
- GET /signals
- POST /evaluate-trade
- POST /paper-trade

## Safety model

- max trade size cap
- max daily loss cap
- max drawdown cap
- no live execution unless explicitly enabled
- emergency shutdown flag

## Roadmap

- [ ] live market data adapter
- [ ] wallet and execution integration
- [ ] persistence layer
- [ ] AI scoring model
- [ ] dashboard and alerts
- [ ] backtesting engine

## Disclaimer

This project is for research and simulation purposes. It should not be used for real trading without a strict testing and audit process.
