from sqlalchemy import Column, Integer, String, ForeignKey

from app.database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    student_id = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True
    )

    program_id = Column(
        Integer,
        ForeignKey("programs.id"),
        nullable=False
    )