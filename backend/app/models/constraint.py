from sqlalchemy import Column, Integer, String, Boolean, Text

from app.database import Base


class Constraint(Base):
    __tablename__ = "constraints"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)

    type = Column(String(20), nullable=False)

    description = Column(Text, nullable=True)

    is_active = Column(Boolean, default=True, nullable=False)

    weight = Column(Integer, default=1, nullable=False)