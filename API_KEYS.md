# API keys and environment configuration

**Rule: no API key or secret is committed to this repository.**

## Required to run or test

None. Tests and paper-trade mode use stub data and deterministic logic.

## Environment variables in `.env.example`

| Variable | Purpose | Key required? |
|---|---|---|
| `ENVIRONMENT`, `APP_NAME`, `APP_PORT` | App configuration | No |
| `MAX_TRADE_USD`, `MAX_DAILY_LOSS_USD`, `MAX_DRAWDOWN_PCT` | Risk limits | No |
| `ENABLE_LIVE_TRADING` | Must stay `false`; there is no execution path | No |
| `EMERGENCY_SHUTDOWN` | Halts evaluation and paper trading | No |
| `AI_MODEL_NAME`, `AI_API_KEY` | Placeholders for a future provider; current scorer is deterministic | No |
| `MARKET_DATA_PROVIDER`, `CHAIN_ID` | Provider selection metadata | No |
| `LOG_LEVEL` | Logging | No |

CoinGecko and DexScreener are called through public endpoints; no key is
configured or required. If you later add a keyed provider, put the key in an
environment variable or a GitHub repository secret — never in source.

## What I did not do

I did not search GitHub for "free" keys or reuse credentials found in public
repos. That would be credential misuse, not configuration.
