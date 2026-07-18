from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    Text,
    DateTime,
    func
)

from sqlalchemy.orm import relationship

from models.base import Base


class HiringProjectNote(Base):

    __tablename__ = "hiring_project_notes"

    id = Column(Integer, primary_key=True)

    project_id = Column(
        Integer,
        ForeignKey("hiring_projects.id", ondelete="CASCADE")
    )

    document_id = Column(
        Integer,
        ForeignKey("hiring_project_documents.id", ondelete="CASCADE"),
        nullable=False
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE")
    )

    content = Column(Text)

    created_at = Column(
        DateTime,
        server_default=func.now()
    )

    user = relationship("User")

    document = relationship(
        "HiringProjectDocument",
        back_populates="notes"
    )
