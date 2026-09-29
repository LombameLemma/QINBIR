from sqlalchemy import Column, Integer, String

from app.database import Base


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)

    building = Column(String(100), nullable=False)

    capacity = Column(Integer, nullable=False)

    room_type = Column(String(50), nullable=False)