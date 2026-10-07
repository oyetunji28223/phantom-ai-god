# Phantom AI God

Phantom AI God is a starter framework for an AI-assisted memecoin sniper and execution system.

This repository is intentionally structured as a safe, testable foundation for:
- market scanning and signal generation
- risk controls and trade guardrails
- execution orchestration
- monitoring and alerting
- future AI model integration

## Project goals
- Discover promising low-cap and mid-cap movement opportunities
- Rank opportunities using a transparent scoring system
- Apply safety checks before any trade decision
- Support a paper-trading mode before real execution
- Provide a clean backend API for monitoring and automation

## Architecture

```text
phantom-ai-god/
├── app/
│   ├── core/
│   ├── services/
│   ├── strategies/
│   ├── config.py
│   ├── main.py
│   └── __init__.py
├── tests/
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
└── scripts/
    └── run_dev.py
```

## Quick start

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

5. Visit the API docs

- Swagger UI: http://localhost:8000/docs
- OpenAPI JSON: http://localhost:8000/openapi.json

## Default endpoints

- GET /health
- GET /signals
- POST /evaluate-trade
- POST /paper-trade

## Safety model

This project includes a layered safety system that is intentionally strict:
- max trade size cap
- maximum drawdown cap
- loss-per-trade guard
- no live execution unless explicitly enabled
- emergency shutdown flag

## Notes

This is a starter implementation focused on a production-friendly structure and safe defaults. It does not execute on-chain transactions by default and should only be run with a paper-trading or sandbox environment.

## Roadmap

- [ ] live market feed integration
- [ ] wallet and blockchain execution adapters
- [ ] AI signal ranking model
- [ ] dashboard UI
- [ ] alerting and monitoring
- [ ] advanced strategy backtesting

## Disclaimer

This project is for educational and research purposes. Do not use it for uncontrolled or real-money trading without proper testing, auditing, and risk controls.
