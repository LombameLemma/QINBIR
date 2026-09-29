from sqlalchemy import Column, Integer, String, ForeignKey

from app.database import Base


class Lecturer(Base):
    __tablename__ = "lecturers"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    department_id = Column(
        Integer,
        ForeignKey("departments.id"),
        nullable=False
    )

    employee_id = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True
    )

    name = Column(String(100), nullable=False)