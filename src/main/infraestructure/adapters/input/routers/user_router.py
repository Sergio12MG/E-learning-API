from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.main.application.services.user_service import UserService
from src.main.domain.exceptions import AccessDenied_Error, User_EmailRepeated_Error, User_NotFound_Error
from src.main.domain.models.user import User
from src.main.infraestructure.adapters.input.dependencies.security import get_current_user
from src.main.infraestructure.adapters.input.schemas.user import UserCreate, UserResponse, UserUpdate, Domain_to_Schema
from src.main.infraestructure.adapters.output.sqlalchemy_user_repo import SQLAlchemy_UserRepository
from src.main.infraestructure.db.database import get_db

from src.main.utils.response import GenericResponse


router = APIRouter(prefix="/api/v1/users", tags=["Users"])

# Injectable service dependency
def get_user_service(db: Session = Depends(get_db)) -> UserService:
    repository = SQLAlchemy_UserRepository(db)
    return UserService(repository)

# ============================================ CREATE ============================================
@router.post("/registration")
def user_registration(user_data: UserCreate, service: UserService = Depends(get_user_service)):
    try:
        # Conversion Schema -> Domain
        # Call the application service
        created_user = service.create_user(
            name=user_data.name,
            email=user_data.email,
            password=user_data.password
        )

        # Conversion Domain -> Schema
        result = Domain_to_Schema(created_user)

        return GenericResponse(
            success=True,
            message="Usuario registrado exitosamente",
            data=result
        )
    except User_EmailRepeated_Error as e:
        raise HTTPException(status_code=400, detail=str(e))

# ============================================ READ ============================================
@router.get("/{user_id}")
def user_by_id(user_id: int, service: UserService = Depends(get_user_service)):
    try:
        # Schema -> Domain
        user = service.find_user_id(user_id)

        # Domain -> Schema
        result = Domain_to_Schema(user)

        return GenericResponse(
            success=True,
            message="Usuario encontrado exitosamente",
            data=result
        )
    except User_NotFound_Error as e:
        raise HTTPException(status_code=404, detail=str(e))

# ============================================ UPDATE ============================================
@router.patch("/{user_id}")
def user_update(user_id: int, user_data: UserUpdate, current_user: User = Depends(get_current_user), service: UserService = Depends(get_user_service)):
    try:
        if current_user.id != user_id:
            raise AccessDenied_Error("No tienes permisos para actualizar este usuario.")

        # Schema -> Domain
        user_to_update = service.update_user(
            user_id=user_id,
            name=user_data.name,
            email=user_data.email,
            password=user_data.password
        )

        # Domain -> Schema
        result = Domain_to_Schema(user_to_update)

        return GenericResponse(
            success=True,
            message="Usuario actualizado exitosamente",
            data=result
        )
    except User_NotFound_Error as e:
        raise HTTPException(status_code=404, detail=str(e))
    except User_EmailRepeated_Error as e:
        raise HTTPException(status_code=400, detail=str(e))
    except AccessDenied_Error as e:
        raise HTTPException(status_code=403, detail=str(e))

# ============================================ DELETE ============================================
@router.delete("/{user_id}")
def user_delete(user_id: int, password: str, service: UserService = Depends(get_user_service)):
    try:
        service.delete_user(user_id, password)

        return GenericResponse(
            success=True,
            message="Usuario eliminado exitosamente",
            data=None
        )
    except User_NotFound_Error as e:
        raise HTTPException(status_code=404, detail=str(e))
