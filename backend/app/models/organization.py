from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from database.db import Base

class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


    users = relationship("User", back_populates="organization", cascade="all, delete")
