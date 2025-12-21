"""Base connector and sink abstractions for conduits pipelines."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class DataConnector(ABC):
    """Interface for anything that can extract data from a source."""

    @abstractmethod
    def extract(self, **overrides: Any) -> Any:  # pragma: no cover - interface
        """Pull data from the backing source and return it."""


class DataSink(ABC):
    """Interface for destinations that accept transformed payloads."""

    @abstractmethod
    def persist(self, payload: Any, **kwargs: Any) -> None:  # pragma: no cover
        """Write the payload to the destination."""
