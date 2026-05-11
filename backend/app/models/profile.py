from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
from database.db import Base

from enum import Enum as PyEnum

class Role(PyEnum):
  Admin = "admin"
  Recruiter = "recruiter"
  Viewer = "viewer"

class Profile(Base):
  __tablename__ = "profiles"

  id = Column(Integer, primary_key=True, index=True)

  first_name = Column(String)
  last_name = Column(String)

  role = Column(Enum(Role), default=Role.Viewer, nullable=False)

  user_id = Column(Integer, ForeignKey("users.id"), unique=True)

  user = relationship(
    "User",
    back_populates="profile"
  )
