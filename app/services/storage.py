from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any


class TradeStore:
    _db_path: Path = Path(__file__).resolve().parents[1] / "data" / "phantom_ai_god.db"

    @classmethod
    def set_db_path(cls, path: str | Path) -> None:
        cls._db_path = Path(path)
        cls.init_db()

    @classmethod
    def init_db(cls) -> None:
        cls._db_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(cls._db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS paper_trades (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    symbol TEXT NOT NULL,
                    action TEXT NOT NULL,
                    confidence REAL NOT NULL,
                    score REAL NOT NULL,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.commit()

    def __init__(self, db_path: str | Path | None = None) -> None:
        if db_path is not None:
            self._db_path = Path(db_path)
        else:
            self._db_path = self.__class__._db_path
        self.init_db()

    def log_trade(self, symbol: str, action: str, confidence: float, score: float) -> None:
        with sqlite3.connect(self._db_path) as conn:
            conn.execute(
                "INSERT INTO paper_trades (symbol, action, confidence, score) VALUES (?, ?, ?, ?)",
                (symbol, action, confidence, score),
            )
            conn.commit()

    def get_recent_trades(self, limit: int = 20) -> list[dict[str, Any]]:
        with sqlite3.connect(self._db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                "SELECT symbol, action, confidence, score, created_at FROM paper_trades ORDER BY id DESC LIMIT ?",
                (max(1, min(limit, 100)),),
            ).fetchall()
        return [dict(row) for row in rows]
