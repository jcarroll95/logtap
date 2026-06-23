from datetime import datetime
from typing import List

from pydantic import BaseModel


class ItemCount(BaseModel):
    name: str # e.g., for IP or Path
    count: int
    class Config:
        from_attributes = True  # This allows Pydantic to read SQLAlchemy objects

class JobResponse(BaseModel):
    lines_total: int
    lines_parsed: int
    lines_skipped: int
    status_classes: dict[str, int]
    total_bytes: int
    top_ips: List[ItemCount]
    top_paths: List[ItemCount]
    timespan_start: datetime
    timespan_end: datetime
    error_rate: float
    class Config:
        from_attributes = True  # This allows Pydantic to read SQLAlchemy objects
