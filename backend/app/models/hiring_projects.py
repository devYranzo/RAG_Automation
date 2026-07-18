from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    DateTime,
    func
)
from sqlalchemy.orm import relationship

from models.base import Base


class HiringProject(Base):
    __tablename__ = "hiring_projects"

    id = Column(Integer, primary_key=True, index=True)

    organization_id = Column(
        Integer,
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False
    )

    created_by = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    title = Column(String(200), nullable=False)
    description = Column(Text)

    search_prompt = Column(Text)

    status = Column(String(20), default="ACTIVE")

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )

    members = relationship(
        "HiringProjectMember",
        back_populates="project",
        cascade="all, delete-orphan"
    )

    documents = relationship(
        "HiringProjectDocument",
        back_populates="project",
        cascade="all, delete-orphan"
    )
