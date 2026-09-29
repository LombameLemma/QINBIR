from sqlalchemy import Column, Integer, String, ForeignKey

from app.database import Base


class StudentSection(Base):
    __tablename__ = "student_sections"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)

    program_id = Column(
        Integer,
        ForeignKey("programs.id"),
        nullable=False
    )

    year = Column(Integer, nullable=False)

    semester = Column(Integer, nullable=False)

    student_count = Column(Integer, nullable=False)