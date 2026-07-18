from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    func, UniqueConstraint
)

from sqlalchemy.orm import relationship

from models.base import Base


class HiringProjectDocument(Base):
    __tablename__ = "hiring_project_documents"
    __table_args__ = (
        UniqueConstraint(
            "project_id",
            "relative_path",
            name="uq_project_document"
        ),
    )

    id = Column(Integer, primary_key=True, index=True)

    project_id = Column(
        Integer,
        ForeignKey("hiring_projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    relative_path = Column(
        String(500),
        nullable=False
    )

    filename = Column(
        String(255),
        nullable=False
    )

    folder = Column(
        String(255),
        nullable=False,
        default="General"
    )

    added_by = Column(
        Integer,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True
    )

    status = Column(
        String(30),
        nullable=False,
        default="PENDING"
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )

    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )

    # ==========================
    # Relationships
    # ==========================

    project = relationship(
        "HiringProject",
        back_populates="documents"
    )

    added_by_user = relationship(
        "User",
        foreign_keys=[added_by],
        back_populates="added_documents"
    )

    notes = relationship(
        "HiringProjectNote",
        back_populates="document",
        cascade="all, delete-orphan"
    )