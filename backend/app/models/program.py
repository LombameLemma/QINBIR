from sqlalchemy import Column, Integer, String, ForeignKey

from app.database import Base


class Program(Base):
    __tablename__ = "programs"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)

    code = Column(String(20), unique=True, nullable=False, index=True)

    department_id = Column(
        Integer,
        ForeignKey("departments.id"),
        nullable=False
    )