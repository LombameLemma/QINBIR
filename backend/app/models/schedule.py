from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.database import Base


class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)

    status = Column(String(30), nullable=False, default="DRAFT")

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    approved_at = Column(DateTime, nullable=True)

    published_at = Column(DateTime, nullable=True)