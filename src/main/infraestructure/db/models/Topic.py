from sqlalchemy import Column, Integer, String, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from src.main.infraestructure.db.database import Base

import enum

class TopicType(str, enum.Enum):
    VIDEO = "video"
    TEXT = "text"
    QUIZ = "quiz"
    ASSIGNMENT = "assignment"

class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, unique=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=True) # HTML content or plain text
    order = Column(Integer, nullable=False, default=0)
    topic_type = Column(String(50), default=TopicType.TEXT.value)
    resource_url = Column(String(500), nullable=True)

    # FK 1:1
    module_id = Column(
        Integer,
        ForeignKey("modules.id", ondelete="CASCADE"),
        nullable=False
    )

    # --- Relation ---
    module = relationship("Module", backref="topics")
