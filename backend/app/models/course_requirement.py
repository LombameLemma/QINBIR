from sqlalchemy import Column, Integer, ForeignKey

from app.database import Base


class CourseRequirement(Base):
    __tablename__ = "course_requirements"

    id = Column(Integer, primary_key=True, index=True)

    course_id = Column(
        Integer,
        ForeignKey("courses.id"),
        nullable=False
    )

    student_section_id = Column(
        Integer,
        ForeignKey("student_sections.id"),
        nullable=False
    )

    lecturer_id = Column(
        Integer,
        ForeignKey("lecturers.id"),
        nullable=False
    )

    sessions_per_week = Column(
        Integer,
        nullable=False,
        default=2
    )

    long_session_hours = Column(
        Integer,
        nullable=False,
        default=2
    )

    short_session_hours = Column(
        Integer,
        nullable=False,
        default=1
    )