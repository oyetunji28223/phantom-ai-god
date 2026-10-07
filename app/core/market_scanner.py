from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TokenSignal:
    symbol: str
    price_usd: float
    liquidity_usd: float
    volume_24h: float
    price_change_pct: float
    volatility: float
    score: float
    action: str


class MarketScanner:
    def __init__(self):
        self._demo_tokens = [
            {"symbol": "DOGE", "price_usd": 0.18, "liquidity_usd": 820000, "volume_24h": 2_400_000, "price_change_pct": 12.4, "volatility": 0.72},
            {"symbol": "PEPE", "price_usd": 0.000018, "liquidity_usd": 630000, "volume_24h": 1_900_000, "price_change_pct": 9.7, "volatility": 0.81},
            {"symbol": "BONK", "price_usd": 0.000028, "liquidity_usd": 540000, "volume_24h": 1_100_000, "price_change_pct": 6.9, "volatility": 0.61},
            {"symbol": "WIF", "price_usd": 1.92, "liquidity_usd": 420000, "volume_24h": 980000, "price_change_pct": -2.1, "volatility": 0.42},
        ]

    def scan(self) -> list[TokenSignal]:
        signals: list[TokenSignal] = []
        for token in self._demo_tokens:
            score = self._score_token(token)
            action = "buy" if score >= 70 else "hold"
            signals.append(
                TokenSignal(
                    symbol=token["symbol"],
                    price_usd=token["price_usd"],
                    liquidity_usd=token["liquidity_usd"],
                    volume_24h=token["volume_24h"],
                    price_change_pct=token["price_change_pct"],
                    volatility=token["volatility"],
                    score=score,
                    action=action,
                )
            )
        return sorted(signals, key=lambda item: item.score, reverse=True)

    @staticmethod
    def _score_token(token: dict) -> float:
        price_change = token["price_change_pct"]
        volume = min(token["volume_24h"] / 2_000_000, 1.0) * 40
        liquidity = min(token["liquidity_usd"] / 1_000_000, 1.0) * 30
        volatility = min(token["volatility"] / 1.0, 1.0) * 30
        momentum = max(min((price_change + 5) * 3.5, 100), 0)

        weighted = volume + liquidity + volatility + momentum
        return round(max(0.0, min(weighted, 100.0)), 2)
