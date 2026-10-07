#!/usr/bin/env python3

from __future__ import annotations

import uvicorn

from app.config import settings
from app.main import app


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=settings.app_port)
