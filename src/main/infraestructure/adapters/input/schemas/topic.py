from typing import Optional

from pydantic import BaseModel, Field

from src.main.domain.models.course import Topic

# Topic registration
class TopicCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=40)
    module_id: int = Field(..., ge=0)
    content: str = Field(min_length=5, max_length=500)
    order: int = Field(..., ge=0)
    topic_type: str = Field(...)
    resource_url: str = Field(min_length=1)

# Topic update
class TopicUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    order: int | None = None
    topic_type: str | None = None
    resource_url: str | None = None

# Response
class TopicResponse(BaseModel):
    id: int
    title: str
    content: Optional[str] = None
    order: int
    topic_type: str
    resource_url: Optional[str] = None
    module_id: int

    class Config:
        from_attributes = True

# Entity converter
def Domain_to_Schema(domain: Topic) -> TopicResponse:
    return TopicResponse(
        id=domain.id,
        title=domain.title,
        content=domain.content,
        order=domain.order,
        topic_type=domain.topic_type,
        resource_url=domain.resource_url,
        module_id=domain.module_id
    )