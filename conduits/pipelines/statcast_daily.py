"""Generalized Statcast ingestion pipeline."""
from __future__ import annotations

from datetime import datetime, timedelta

from ..connectors.filesystem import CSVFolderSink
from ..connectors.statcast import StatcastConnector
from .base import BasePipeline


class StatcastDailyPipeline(BasePipeline):
    """Pulls and writes Statcast-derived daily aggregates."""

    def __init__(self, start: str, end: str, out_folder: str) -> None:
        connector = StatcastConnector(start, end)
        sink = CSVFolderSink(out_folder)
        super().__init__("statcast_daily", connector, sink, transform=self._transform)

    @staticmethod
    def _transform(frame):  # type: ignore[override]
        """Minimal transform placeholder (extend with domain logic)."""
        frame = frame.copy()
        frame["game_date"] = frame["game_date"].astype(str)
        return {"statcast_events": frame}

    @classmethod
    def covering_current_season(cls, out_folder: str) -> "StatcastDailyPipeline":
        opening_day = datetime(datetime.today().year, 3, 1).strftime("%Y-%m-%d")
        yesterday = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")
        return cls(opening_day, yesterday, out_folder)
