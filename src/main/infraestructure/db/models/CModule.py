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
        backref="parent", # Create automatically the 'parent' property
        remote_side=[id], # Indicates which column is the 'parent'
        cascade="all, delete-orphan",
        single_parent=True,
        lazy="selectin" # Efficient loading of child elements
    )

    # Towards the themes
    topics = relationship(
        "Topic",
        back_populates="module",
        cascade="all, delete-orphan",
        lazy="selectin",
        order_by="Topic.order"
    )
