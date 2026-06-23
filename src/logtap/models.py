"""
The models.py module contains ORM-layer definitions for SQLAlchemy classes defining tables in our persistence layer. The
current JobRecord object defines our postgres job table.
"""

from datetime import datetime
from typing import List
from sqlalchemy.orm import Mapped, mapped_column
from logtap.database import Base
from logtap.schemas import ItemCount

class JobRecord(Base):
    __tablename__ = "jobs"

    # Primary Key
    id: Mapped[int] = mapped_column(primary_key=True)

    lines_total: Mapped[int] = mapped_column()
    lines_parsed: Mapped[int] = mapped_column()
    lines_skipped: Mapped[int] = mapped_column()
    status_classes: Mapped[dict[str, int]]  = mapped_column()
    total_bytes: Mapped[int] = mapped_column()
    top_ips: Mapped[List[ItemCount]] = mapped_column()
    top_paths: Mapped[List[ItemCount]] = mapped_column()
    timespan_start: Mapped[datetime] = mapped_column()
    timespan_end: Mapped[datetime] = mapped_column()

    # ... other fields ...
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    @property
    def is_active(self) -> bool:
        return True