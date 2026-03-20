from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.main.infraestructure.db.database import get_db
from src.main.infraestructure.adapters.output.sqlalchemy_user_repo import SQLAlchemy_UserRepository
from src.main.application.services.auth_service import AuthService
from src.main.infraestructure.adapters.input.schemas.user import UserLogin, Token
from src.main.utils.response import GenericResponse


router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])

# Injectable service dependency
def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    repository = SQLAlchemy_UserRepository(db)
    return AuthService(repository)

@router.post("/login")
def login (login_data: UserLogin, service: AuthService = Depends(get_auth_service)):
    # 1. Authentication of the user data
    user = service.authenticate_user(login_data.email, login_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 2. Generate the token
    access_token = service.create_token_for_user(user)

    token_response = Token(
        access_token=access_token,
        token_type="bearer",
        user={
            "id": user.id,
            "name": user.name,
            "email": user.email
        }
    )

    return GenericResponse(
        success=True,
        message="Login exitoso",
        data=token_response
    )