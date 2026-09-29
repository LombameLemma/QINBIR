from sqlalchemy import Column, Integer, String, ForeignKey

from app.database import Base


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)

    code = Column(String(20), unique=True, nullable=False, index=True)

    name = Column(String(150), nullable=False)

    credit_hours = Column(Integer, nullable=False)

    program_id = Column(
        Integer,
        ForeignKey("programs.id"),
        nullable=False
    )