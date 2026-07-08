from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.main.application.services.topic_service import TopicService
from src.main.domain.exceptions import AccessDenied_Error, Topic_NotFound_Exception, Module_NotFound_Error
from src.main.domain.models.user import User
from src.main.infraestructure.adapters.input.dependencies.security import get_current_user
from src.main.infraestructure.adapters.input.schemas.topic import TopicCreate, TopicUpdate, Domain_to_Schema
from src.main.infraestructure.adapters.output.sqlalchemy_topic_repo import SQLAlchemy_TopicRepository
from src.main.infraestructure.adapters.output.sqlalchemy_module_repo import SQLAlchemy_ModuleRepository
from src.main.infraestructure.adapters.output.sqlalchemy_course_repo import SQLAlchemy_CourseRepository
from src.main.infraestructure.adapters.output.sqlalchemy_user_repo import SQLAlchemy_UserRepository
from src.main.infraestructure.db.database import get_db

from src.main.utils.response import GenericResponse


router = APIRouter(prefix="/api/v1/topics", tags=["Topics"])

# Injectable service dependency
def get_topic_service(db: Session = Depends(get_db)) -> TopicService:
    topic_repo = SQLAlchemy_TopicRepository(db)
    module_repo = SQLAlchemy_ModuleRepository(db)
    course_repo = SQLAlchemy_CourseRepository(db)
    user_repo = SQLAlchemy_UserRepository(db)
    return TopicService(topic_repo, module_repo, course_repo, user_repo)

# ============================================ CREATE ============================================
@router.post("/create")
def topic_creation(topic_data: TopicCreate, service: TopicService = Depends(get_topic_service), current_user: User = Depends(get_current_user)):
    try:
        # Conversion Schema -> Domain
        created_topic = service.create_topic(
            title=topic_data.title,
            module_id=topic_data.module_id,
            content=topic_data.content,
            resource_url=topic_data.resource_url,
            order=topic_data.order,
            topic_type=topic_data.topic_type,
        )

        # Conversion Domain -> Schema
        result = Domain_to_Schema(created_topic)

        return GenericResponse(
            success=True,
            message="Tema creado exitosamente",
            data=result
        )
    except Module_NotFound_Error as e:
        raise HTTPException(status_code=404, detail=str(e))
    except AccessDenied_Error as e:
        raise HTTPException(status_code=401, detail=str(e))
    
# ============================================ READ ============================================
@router.get("/{topic_id}") # By ID
def topic_by_id(topic_id: int, service: TopicService = Depends(get_topic_service)):
    try:
        topic = service.find_topic_id(topic_id)

        # Conversion Domain -> Schema
        result = Domain_to_Schema(topic)

        return GenericResponse(
            success=True,
            message="Tema encontrado exitosamente",
            data=result
        )
    except Topic_NotFound_Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.get("/title/") # By title
def topic_by_title(title: str, service: TopicService = Depends(get_topic_service)):
    try:
        topic = service.find_topic_title(title)

        # Conversion Domain -> Schema
        result = Domain_to_Schema(topic)

        return GenericResponse(
            success=True,
            message="Tema encontrado exitosamente",
            data=result
        )
    except Topic_NotFound_Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.get("/{module_id}/tree") # Topics inside a module
def topic_tree(module_id: int, service: TopicService = Depends(get_topic_service)):
    try:
        topics = service.find_all_topics(module_id)

        # Conversion Domain -> Schema
        result = [Domain_to_Schema(topic) for topic in topics]

        return GenericResponse(
            success=True,
            message="Temas encontrados exitosamente",
            data=result
        )
    except Module_NotFound_Error as e:
        raise HTTPException(status_code=404, detail=str(e))
    
# ============================================ UPDATE ============================================
@router.patch("/{topic_id}")
def topic_update(topic_id: int, topic_data: TopicUpdate, service: TopicService = Depends(get_topic_service), current_user: User = Depends(get_current_user)):
    try :
        topic_to_update = service.update_topic(
            topic_id=topic_id,
            title=topic_data.title,
            content=topic_data.content,
            order=topic_data.order,
            topic_type=topic_data.topic_type,
            resource_url=topic_data.resource_url
        )

        # Conversion Domain -> Schema
        result = Domain_to_Schema(topic_to_update)

        return GenericResponse(
            success=True,
            message="Tema actualizado exitosamente",
            data=result
        )
    except Topic_NotFound_Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    except AccessDenied_Error as e:
        raise HTTPException(status_code=401, detail=str(e))
    
# ============================================ DELETE ============================================
@router.delete("/{topic_id}")
def topic_delete(topic_id: int, service: TopicService = Depends(get_topic_service), current_user: User = Depends(get_current_user)):
    try:
        service.delete_topic(topic_id)

        return GenericResponse(
            success=True,
            message="Tema eliminado exitosamente",
            data=None
        )
    except Topic_NotFound_Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    except AccessDenied_Error as e:
        raise HTTPException(status_code=401, detail=str(e))