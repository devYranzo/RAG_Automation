from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    String,
    DateTime,
    func
)

from sqlalchemy.orm import relationship

from models.base import Base


class HiringProjectMember(Base):
    __tablename__ = "hiring_project_members"

    id = Column(Integer, primary_key=True)

    project_id = Column(
        Integer,
        ForeignKey("hiring_projects.id", ondelete="CASCADE")
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE")
    )

    role = Column(
        String(20),
        default="RECRUITER"
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )

    project = relationship(
        "HiringProject",
        back_populates="members"
    )

    user = relationship("User")