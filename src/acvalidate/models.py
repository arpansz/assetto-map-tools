from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum


class Severity(str, Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass(frozen=True)
class Finding:
    severity: Severity
    code: str
    message: str
    source: str | None = None
    line: int | None = None

    def to_dict(self) -> dict:
        data = asdict(self)
        data["severity"] = self.severity.value
        return data
