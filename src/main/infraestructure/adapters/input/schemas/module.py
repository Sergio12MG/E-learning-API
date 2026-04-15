from typing import List, Optional

from pydantic import BaseModel, Field

from src.main.domain.models.course import CModule

# Module registration
class ModuleCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    course_id: int = Field(..., ge=1)
    order: int = Field(..., ge=0)
    is_published: bool = Field(...)
    description: str = Field(min_length=5, max_length=500)
    parent_id: int = Field(ge=1)

# Module update
class ModuleUpdate(BaseModel):
    module_id: int | None = None
    title: str | None = None
    order: int | None = None
    is_published: bool | None = None
    description: str | None = None
    parent_id: int | None = None

# Response
class ModuleResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    order: int
    is_published: bool
    course_id: int
    parent_id: int
    submodules: List['ModuleResponse'] = []

    class Config:
        orm_mode = True
    
# Entity converter
def Domain_to_Schema(domain: CModule) -> ModuleResponse:
    return ModuleResponse(
        id=domain.id,
        title=domain.title,
        description=domain.description,
        order=domain.order,
        is_published=domain.is_published,
        course_id=domain.course_id,
        parent_id=domain.parent_id,
        submodules=domain.submodules
    )