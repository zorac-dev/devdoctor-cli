from dataclasses import dataclass
from enum import Enum


class Status(str, Enum):
    OK = "ok"
    MISSING = "missing"
    ERROR = "error"


@dataclass(frozen=True)
class CheckResult:
    name: str
    status: Status
    version: str | None = None
    message: str | None = None
