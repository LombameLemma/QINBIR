from sqlalchemy import Column, Integer, String, Time

from app.database import Base


class TimeSlot(Base):
    __tablename__ = "time_slots"

    id = Column(Integer, primary_key=True, index=True)

    day = Column(String(20), nullable=False)

    start_time = Column(Time, nullable=False)

    end_time = Column(Time, nullable=False)