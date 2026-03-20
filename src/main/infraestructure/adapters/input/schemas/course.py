from pydantic import BaseModel, Field

# Course registration
class CourseCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=150)
    description: str = Field(min_length=5)
    user_id: int = Field(..., ge=1)

# Course update
class CourseUpdate(BaseModel):
    title: str | None = None
    description: str | None = None

# Response
class CourseResponse(BaseModel):
    id: int
    title: str
    description: str
    user_id: int

    class Config:
        orm_mode=True
