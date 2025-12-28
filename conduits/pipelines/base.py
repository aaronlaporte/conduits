"""Reusable pipeline definitions."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable

from ..connectors.base import DataConnector, DataSink


@dataclass
class PipelineContext:
    """Runtime metadata made available to hooks."""

    name: str
    started_at: datetime = field(default_factory=datetime.utcnow)
    metadata: dict[str, Any] = field(default_factory=dict)


class BasePipeline:
    """Composable extract-transform-load pipeline."""

    def __init__(
        self,
        name: str,
        connector: DataConnector,
        sink: DataSink,
        transform: Callable[[Any], Any] | None = None,
    ) -> None:
        self.name = name
        self.connector = connector
        self.sink = sink
        self.transform = transform

    def _infer_record_count(self, payload: Any) -> Any:
        if hasattr(payload, "shape"):
            return getattr(payload, "shape")
        if isinstance(payload, dict):
            for value in payload.values():
                count = self._infer_record_count(value)
                if count is not None:
                    return count
        if isinstance(payload, (list, tuple, set)):
            return len(payload)
        return None

    def run(self, **kwargs: Any) -> PipelineContext:
        ctx = PipelineContext(name=self.name)
        raw = self.connector.extract(**kwargs)
        payload = self.transform(raw) if self.transform else raw
        self.sink.persist(payload)
        ctx.metadata["records"] = self._infer_record_count(payload)
        return ctx
