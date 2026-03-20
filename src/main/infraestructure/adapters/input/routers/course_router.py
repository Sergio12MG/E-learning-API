from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.main.application.services.course_service import CourseService
from src.main.application.validators.course_validators import Course_Existence_Validator, Course_Return_Validator
from src.main.application.validators.user_validators import UserBasicValidator
from src.main.domain.exceptions import AccessDenied_Error, Course_NotFound_Error, Course_TitleRepeated_Error, User_NotFound_Error
from src.main.infraestructure.adapters.input.schemas.course import CourseCreate, CourseResponse, CourseUpdate
from src.main.infraestructure.adapters.output.sqlalchemy_course_repo import SQLAlchemy_CourseRepository
from src.main.infraestructure.adapters.output.sqlalchemy_user_repo import SQLAlchemy_UserRepository
from src.main.infraestructure.db.database import get_db

from src.main.utils.response import GenericResponse


router = APIRouter(prefix="/api/v1/courses", tags=["Courses"])

# Injectable service dependency
def get_course_service(db: Session = Depends(get_db)) -> CourseService:
    course_repo = SQLAlchemy_CourseRepository(db)
    user_repo = SQLAlchemy_UserRepository(db)
    return CourseService(course_repo, user_repo)

# ============================================ CREATE ============================================
@router.post("/create")
def course_creation(course_data: CourseCreate, service: CourseService = Depends(get_course_service)):
    try:
        # Conversion Schema -> Domain
        # Call the application service
        created_course = service.create_course(
            title=course_data.title,
            description=course_data.description,
            user_id=course_data.user_id
        )

        # Conversion Domain -> Pydantic
        result = CourseResponse(
            id=created_course.id,
            title=created_course.title,
            description=created_course.description,
            user_id=created_course.user_id
        )

        return GenericResponse(
            success=True,
            message="Curso creado exitosamente",
            data=result
        )
    except Course_TitleRepeated_Error as e:
        raise HTTPException(status_code=400, detail=str(e))
    except User_NotFound_Error as e:
        raise HTTPException(status_code=404, detail=str(e))

# ============================================ READ ============================================
@router.get("/{course_id}")
def course_by_id(course_id: int, service: CourseService = Depends(get_course_service)):
    try:
        course = service.find_course_id(course_id)

        result = CourseResponse(
            id=course.id,
            title=course.title,
            description=course.description,
            user_id=course.user_id
        )

        return GenericResponse(
            success=True,
            message="Curso encontrado exitosamente",
            data=result
        )
    except Course_NotFound_Error as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.get("/{title}")
def course_by_title(title: str, service: CourseService = Depends(get_course_service)):
    try:
        course = service.find_course_title(title)

        result = CourseResponse(
            id=course.id,
            title=course.title,
            description=course.description,
            user_id=course.user_id
        )

        return GenericResponse(
            success=True,
            message="Curso encontrado exitosamente",
            data=result
        )
    except Course_NotFound_Error as e:
        raise HTTPException(status_code=404, detail=str(e))
    
# ============================================ UPDATE ============================================
@router.patch("/{course_id}/{user_id}")
def course_update(course_id: int, user_id: int, course_data: CourseUpdate, service: CourseService = Depends(get_course_service)):
    try:
        course_to_update = service.update_course(
            course_id=course_id,
            useR_id=user_id,
            title=course_data.title,
            description=course_data.description
        )

        result = CourseResponse(
            id=course_to_update.id,
            title=course_to_update.title,
            description=course_to_update.description,
            user_id=course_to_update.user_id
        )

        return GenericResponse(
            success=True,
            message="Curso actualizado exitosamente",
            data=result
        )
    except Course_NotFound_Error as e:
        raise HTTPException(status_code=404, detail=str(e))
    except AccessDenied_Error as e:
        raise HTTPException(status_code=403, detail=str(e))
    
# ============================================ DELETE ============================================
@router.delete("/{course_id}/{user_id}")
def course_delete(course_id: int, user_id: int, service: CourseService = Depends(get_course_service)):
    try:
        service.delete_course(course_id, user_id)

        return GenericResponse(
            success=True,
            message="Curso eliminado exitosamente",
            data=None
        )
    except Course_NotFound_Error as e:
        raise HTTPException(status_code=404, detail=str(e))
    except AccessDenied_Error as e:
        raise HTTPException(status_code=403, detail=str(e))
