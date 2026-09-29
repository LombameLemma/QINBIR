from sqlalchemy import Column, Integer, ForeignKey

from app.database import Base


class ScheduleEntry(Base):
    __tablename__ = "schedule_entries"

    id = Column(Integer, primary_key=True, index=True)

    schedule_id = Column(
        Integer,
        ForeignKey("schedules.id"),
        nullable=False
    )

    course_requirement_id = Column(
        Integer,
        ForeignKey("course_requirements.id"),
        nullable=False
    )

    lecturer_id = Column(
        Integer,
        ForeignKey("lecturers.id"),
        nullable=False
    )

    student_section_id = Column(
        Integer,
        ForeignKey("student_sections.id"),
        nullable=False
    )

    room_id = Column(
        Integer,
        ForeignKey("rooms.id"),
        nullable=False
    )

    time_slot_id = Column(
        Integer,
        ForeignKey("time_slots.id"),
        nullable=False
    )