from pydantic import BaseModel, EmailStr, Field

from src.main.domain.models.user import User

# =========== BASIC SCHEMAS ===========
# User registration
class UserCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=255)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=50)

    class Config:
        extra = "forbid"

# User update
class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    password: str | None = None

    class Config:
        extra = "forbid"

# Response
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        orm_mode = True

# =========== AUTH SCHEMAS ===========
# Log-in
class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=8)

# Token for response
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict | None = None # Basic user data

class TokenData(BaseModel):
    user_id: int | None = None
    email: str | None = None

# Entity converter
def Domain_to_Schema(domain: User) -> UserResponse:
    return UserResponse(
        id=domain.id,
        name=domain.name,
        email=domain.email
    )