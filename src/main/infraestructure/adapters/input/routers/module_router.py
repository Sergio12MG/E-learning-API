from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.main.application.services.module_service import ModuleService
from src.main.domain.exceptions import AccessDenied_Error, Module_NotFound_Error, ParentModule_NotFound_Error
from src.main.domain.models.user import User
from src.main.infraestructure.adapters.input.dependencies.security import get_current_user
from src.main.infraestructure.adapters.input.schemas.module import ModuleCreate, ModuleUpdate, ModuleResponse, Domain_to_Schema
from src.main.infraestructure.adapters.output.sqlalchemy_module_repo import SQLAlchemy_ModuleRepository
from src.main.infraestructure.adapters.output.sqlalchemy_course_repo import SQLAlchemy_CourseRepository
from src.main.infraestructure.adapters.output.sqlalchemy_user_repo import SQLAlchemy_UserRepository
from src.main.infraestructure.db.database import get_db

from src.main.utils.response import GenericResponse


router = APIRouter(prefix="/api/v1/modules", tags=["Modules"])

# Injectable service dependency
def get_module_service(db: Session = Depends(get_db)) -> ModuleService:
    module_repo = SQLAlchemy_ModuleRepository(db)
    course_repo = SQLAlchemy_CourseRepository(db)
    user_repo = SQLAlchemy_UserRepository(db)
    return ModuleService(module_repo, course_repo, user_repo)

# ============================================ CREATE ============================================
@router.post("/create")
def module_creation(module_data: ModuleCreate, service: ModuleService = Depends(get_module_service), current_user: User = Depends(get_current_user)):
    try:
        # Conversion Schema -> Domain
        created_module = service.create_module(
            title=module_data.title,
            course_id=module_data.course_id,
            order=module_data.order,
            is_published=module_data.is_published,
            description=module_data.description,
            parent_id=module_data.parent_id
        )

        # Conversion Domain -> Schema
        result = Domain_to_Schema(created_module)

        return GenericResponse(
            success=True,
            message="Módulo craedo exitosamente",
            data=result
        )
    except ParentModule_NotFound_Error as e:
        raise HTTPException(status_code=404, detail=str(e))
    
# ============================================ READ ============================================
@router.get("/{module_id}") # By ID
def module_by_id(module_id: int, service: ModuleService = Depends(get_module_service)):
    try:
        module = service.find_module_id(module_id)

        # Conversion Domain -> Schema
        result = Domain_to_Schema(module, include_children=False)

        return GenericResponse(
            success=True,
            message="Módulo encontrado exitosamente",
            data=result
        )
    except Module_NotFound_Error as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/{title}") # By title
def module_by_title(title: str, service: ModuleService = Depends(get_module_service)):
    try:
        module = service.find_module_title(title)

        # Conversion Domain -> Schema
        result = Domain_to_Schema(module, include_children=False)

        return GenericResponse(
            success=True,
            message="Módulo encontrado exitosamente",
            data=result
        )
    except Module_NotFound_Error as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.get("/{module_id}/tree") # First-level children modules
def module_tree(module_id: int, service: ModuleService = Depends(get_module_service)):
    try:
        module = service.find_child_modules(module_id)

        # Conversion Domain -> schema
        result = Domain_to_Schema(module, include_children=True)

        return GenericResponse(
            success=True,
            message="Módulos obtenidos con éxito",
            data=result
        )
    except ParentModule_NotFound_Error as e:
        raise HTTPException(status_code=404, detail=str(e))
    
# ============================================ UPDATE ============================================
@router.patch("/{module_id}")
def module_update(module_id: int, module_data: ModuleUpdate, service: ModuleService = Depends(get_module_service), current_user: User = Depends(get_current_user)):
    try:
        module_to_update = service.update_module(
            module_id=module_id,
            title=module_data.title,
            order=module_data.order,
            is_published=module_data.is_published,
            description=module_data.description,
            parent_id=module_data.parent_id
        )

        # Conversion Domain -> Schema
        result = Domain_to_Schema(module_to_update)

        return GenericResponse(
            success=True,
            message="Módulo actualizado exitosamente",
            data=result
        )
    except Module_NotFound_Error as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ParentModule_NotFound_Error as e:
        raise HTTPException(status_code=404, detail=str(e))
    
# ============================================ DELETE ============================================
@router.delete("{module_id}")
def module_delete(module_id: int, service: ModuleService = Depends(get_module_service), current_user: User = Depends(get_current_user)):
    try:
        service.delete_module(module_id, current_user.id)

        return GenericResponse(
            success=True,
            message="Módulo eliminado exitosamente",
            data=None
        )
    except Module_NotFound_Error as e:
        raise HTTPException(status_code=404, detail=str(e))
    except AccessDenied_Error as e:
        raise HTTPException(status_code=403, detail=str(e))
        