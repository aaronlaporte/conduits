"""Simple filesystem sinks used in examples."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd

from .base import DataSink


class CSVFolderSink(DataSink):
    """Writes each named DataFrame to ``folder/name.csv``."""

    def __init__(self, folder: str | Path, mode: str = "w") -> None:
        self.folder = Path(folder)
        self.folder.mkdir(parents=True, exist_ok=True)
        self.mode = mode

    def persist(self, payload: dict[str, pd.DataFrame], **kwargs: Any) -> None:
        for name, frame in payload.items():
            out_path = self.folder / f"{name}.csv"
            frame.to_csv(out_path, index=False, mode=self.mode)


class JSONSink(DataSink):
    """Writes JSON-serializable payloads to a file."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def persist(self, payload: Any, **kwargs: Any) -> None:
        with self.path.open("w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=2, default=str)
