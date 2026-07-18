from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from models.base import Base, HasOrganization

class User(Base, HasOrganization):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    is_active = Column(Boolean, default=True)

    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    profile = relationship(
        "Profile",
        back_populates="user",
        uselist=False,
        cascade="all, delete"
    )

    organization = relationship("Organization", back_populates="users")
    projects = relationship("HiringProjectMember", back_populates="users")
