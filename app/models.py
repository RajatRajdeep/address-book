from sqlalchemy import Boolean, Column, Float, Integer

from .database import Base


class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    is_deleted = Column(Boolean, default=False)
