from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.main.infraestructure.db.database import Base

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, unique=True, index=True)
    title = Column(String(50), unique=True, nullable=False)
    description = Column(String(255), nullable=True)

    # FK
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    # 1:1
    user = relationship("User", back_populates="courses")

    # 1:N
    modules = relationship(
        "CModule",
        back_populates="course",
        cascade="all, delete-orphan"
    )
