from typing import Optional

from fastapi import Depends, HTTPException, Header, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from src.main.infraestructure.db.database import get_db
from src.main.infraestructure.adapters.output.sqlalchemy_user_repo import SQLAlchemy_UserRepository
from src.main.domain.models.user import User
from src.main.utils.auth import decode_token

# Target to the endpoint of authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

# Endpoint protection
async def get_current_user(authorization: Optional[str] = Header(None), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales no válidas",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # 1. Check the existence of the header Authorization
    if authorization is None:
        raise credentials_exception
    
    # 2. Get the token from the format "Bearer <token>"
    if not authorization.startswith("Bearer "):
        raise credentials_exception
    
    token = authorization.split(" ")[1]
    
    # 3. Decode the token
    payload = decode_token(token)
    if payload is None:
        raise credentials_exception
    
    # 4. Load the user id from the decoded token
    user_id: str = payload.get("sub")
    if user_id is None:
        raise credentials_exception
    
    # 5. Find the user
    repository = SQLAlchemy_UserRepository(db)
    user = repository.find_by_id(int(user_id))

    if user is None:
        raise credentials_exception
    
    return user

