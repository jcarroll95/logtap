"""
The models.py module contains dataclass definitions for the LogLine, ParseStats, and Report objects used throughout the
logtap application. The LogLine object represents a single line of log data parsed from a log file, while the ParseStats
object tracks the total, parsed, and skipped log lines during parsing. The Report object aggregates and summarizes the
parsed log data for reporting purposes.
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class LogLine:
    client_ip: str
    identity: str
    user: str
    timestamp: datetime
    request_method: str
    request_uri: str
    request_protocol: str
    status_code: int | None
    response_size: int | None
    referrer: str
    user_agent: str


@dataclass
class ParseStats:
    total: int = 0
    parsed: int = 0
    skipped: int = 0


@dataclass(frozen=True)
class Report:
    lines_total: int
    lines_parsed: int
    lines_skipped: int
    status_classes: dict[str, int]
    total_bytes: int
    top_ips: list[tuple[str, int]]
    top_paths: list[tuple[str, int]]
    timespan_start: datetime
    timespan_end: datetime
    @property
    def error_rate(self) -> float:
        if self.lines_parsed == 0:
            return 0.0
        rate = (self.status_classes["4xx"] + self.status_classes["5xx"]) / self.lines_parsed
        return round(rate * 100, 2)
