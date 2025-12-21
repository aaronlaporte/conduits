"""Statcast connector used by MLB-style ingestion pipelines."""
from __future__ import annotations

from datetime import date
from typing import Any

from pybaseball import statcast

from .base import DataConnector


def _normalize_date(value: str | date) -> str:
    if isinstance(value, date):
        return value.strftime("%Y-%m-%d")
    return str(value)


class StatcastConnector(DataConnector):
    """Wraps ``pybaseball.statcast`` with a small abstraction layer."""

    def __init__(self, start_date: str | date, end_date: str | date) -> None:
        self.start_date = _normalize_date(start_date)
        self.end_date = _normalize_date(end_date)

    def extract(self, **overrides: Any):  # type: ignore[override]
        start = overrides.get("start_date", self.start_date)
        end = overrides.get("end_date", self.end_date)
        return statcast(start, end)
