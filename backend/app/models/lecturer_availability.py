from sqlalchemy import Column, Integer, Boolean, ForeignKey

from app.database import Base


class LecturerAvailability(Base):
    __tablename__ = "lecturer_availability"

    id = Column(Integer, primary_key=True, index=True)

    lecturer_id = Column(
        Integer,
        ForeignKey("lecturers.id"),
        nullable=False
    )

    time_slot_id = Column(
        Integer,
        ForeignKey("time_slots.id"),
        nullable=False
    )

    is_available = Column(Boolean, default=True, nullable=False)