from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from conf.database import Base
import uuid


class Store(Base):
    __tablename__ = "store"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String)
    description = Column(String)
    geohash = Column(String)
    drops = relationship("Drop", back_populates="")


class Drop(Base):
    __tablename__ = "drop"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String)
    description = Column(String)
    image_url = Column(String)

    store_id = Column(UUID(as_uuid=True), ForeignKey("store.id"))
    store = relationship("Store", back_populates="drops")

    poaps = relationship("Poap", back_populates="drop")


class Poap(Base):
    __tablename__ = "poap"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    url = Column(String)
    claimed_by = Column(String, nullable=True)
    drop_id = Column(UUID(as_uuid=True), ForeignKey("drop.id"))
    drop = relationship("Drop", back_populates="poaps")
