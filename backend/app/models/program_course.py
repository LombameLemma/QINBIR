from sqlalchemy import Column, Integer, ForeignKey

from app.database import Base


class ProgramCourse(Base):
    __tablename__ = "program_courses"

    id = Column(Integer, primary_key=True, index=True)

    program_id = Column(
        Integer,
        ForeignKey("programs.id"),
        nullable=False,
        index=True
    )

    course_id = Column(
        Integer,
        ForeignKey("courses.id"),
        nullable=False,
        index=True
    )