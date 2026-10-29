"""Weekly performance report: summarize an Excel tracking log into weekly metrics."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd

from ..connectors.excel import ExcelTableConnector
from ..connectors.filesystem import JSONSink
from ..connectors.base import DataSink
from .base import BasePipeline


@dataclass
class WeeklyReportSink(DataSink):
    """Simplified sink that writes summary stats to JSON."""

    path: Path

    def persist(self, payload: Any, **kwargs: Any) -> None:  # type: ignore[override]
        JSONSink(self.path).persist(payload)


class WeeklyPerformanceReportPipeline(BasePipeline):
    """Transforms an Excel log into summary metrics."""

    def __init__(self, workbook: str, sheet: str, out_path: str | Path) -> None:
        connector = ExcelTableConnector(workbook, sheet)
        sink = WeeklyReportSink(Path(out_path))
        super().__init__("weekly_performance_report", connector, sink, transform=self._transform)

    @staticmethod
    def _transform(frame: pd.DataFrame) -> dict[str, Any]:
        frame = frame.dropna(subset=["date", "odds", "amount"]).copy()
        frame["date"] = pd.to_datetime(frame["date"])
        frame["profit"] = frame.apply(_calc_profit_row, axis=1)
        summary = frame.groupby("bet_type").agg(
            total_bets=("id", "count"),
            net_profit=("profit", "sum"),
            staked=("amount", "sum"),
        )
        summary["roi"] = summary["net_profit"] / summary["staked"].replace({0: pd.NA})
        return {
            "date_start": frame["date"].min().strftime("%Y-%m-%d"),
            "date_end": frame["date"].max().strftime("%Y-%m-%d"),
            "summary": summary.reset_index().to_dict(orient="records"),
        }


def _calc_profit_row(row: pd.Series) -> float:
    win = row.get("win")
    odds = row["odds"]
    amount = row["amount"]
    if pd.isna(win):
        return 0.0
    if bool(win):
        return amount * (odds / 100.0) if odds > 0 else amount * (100.0 / abs(odds))
    return -amount
