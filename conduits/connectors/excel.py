"""Excel workbook connectors used for reporting pipelines."""
from __future__ import annotations

from typing import Any

import pandas as pd

from .base import DataConnector


class ExcelTableConnector(DataConnector):
    """Loads a single sheet from an Excel workbook into a DataFrame."""

    def __init__(self, path: str, sheet_name: str) -> None:
        self.path = path
        self.sheet_name = sheet_name

    def extract(self, **overrides: Any) -> pd.DataFrame:  # type: ignore[override]
        sheet = overrides.get("sheet_name", self.sheet_name)
        frame = pd.read_excel(self.path, sheet_name=sheet, engine="openpyxl")
        frame.columns = [str(c).strip().lower() for c in frame.columns]
        return frame
