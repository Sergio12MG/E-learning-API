from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from src.main.infraestructure.db.database import Base

class CModule(Base):
    __tablename__ = "modules"

    id = Column(Integer, primary_key=True, unique=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(String(500), nullable=True)
    order = Column(Integer, nullable=False, default=0)
    is_published = Column(Boolean, default=False)

    # FK
    course_id = Column(
        Integer,
        ForeignKey("courses.id", ondelete="CASCADE"),
        nullable=False
    )

    # Self-referential FK
    parent_id = Column(
        Integer,
        ForeignKey("modules.id", ondelete="CASCADE"),
        nullable=True
    )

    # --- Relations ---

    # 1:1 (Towards the course)
    course = relationship("Course", back_populates="modules")

    # Towards the submodules
    submodules = relationship(
        "CModule",
        back_populates="parent_module",
        remote_side=[id],
        foreign_keys=[parent_id],
        lazy="selectin" # Efficient loading of child elements
    )

    # Parent module reference
    parent_module = relationship(
        "CModule",
        back_populates="submodules",
        foreign_keys=[parent_id]
    )

    # Towards the themes
    topics = relationship(
        "Topic",
        back_populates="module",
        cascade="all, delete-orphan",
        lazy="selectin",
        order_by="Topic.order"
    )
