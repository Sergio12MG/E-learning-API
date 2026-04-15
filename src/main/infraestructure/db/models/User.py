from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.main.infraestructure.db.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, unique=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)

    # 1:N
    courses = relationship(
        "Course",
        back_populates="user",
        cascade="all, delete-orphan"
    )