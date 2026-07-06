from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.main.application.services.course_service import CourseService
from src.main.domain.exceptions import AccessDenied_Error, Course_NotFound_Error, Course_TitleRepeated_Error, User_NotFound_Error
from src.main.domain.models.user import User
from src.main.infraestructure.adapters.input.dependencies.security import get_current_user
from src.main.infraestructure.adapters.input.schemas.course import CourseCreate, CourseResponse, CourseUpdate, Domain_to_Schema
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
def course_creation(course_data: CourseCreate, service: CourseService = Depends(get_course_service), current_user: User = Depends(get_current_user)):
    try:
        # Conversion Schema -> Domain
        # Call the application service
        created_course = service.create_course(
            title=course_data.title,
            description=course_data.description,
            user_id=current_user.id
        )

        # Conversion Domain -> Schema
        result = Domain_to_Schema(created_course)

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
        # Conversion Schema -> Domain
        course = service.find_course_id(course_id)

        # Conversion Domain -> Schema
        result = Domain_to_Schema(course)

        return GenericResponse(
            success=True,
            message="Curso encontrado exitosamente",
            data=result
        )
    except Course_NotFound_Error as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.get("/title/")
def course_by_title(title: str, service: CourseService = Depends(get_course_service)):
    try:
        # Conversion Schema -> Domain
        course = service.find_course_title(title)

        # Conversion Domain -> Schema
        result = Domain_to_Schema(course)

        return GenericResponse(
            success=True,
            message="Curso encontrado exitosamente",
            data=result
        )
    except Course_NotFound_Error as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/author/{author_id}")
def course_by_author(author_id: int, service: CourseService = Depends(get_course_service)):
    try:
        courses = service.find_course_by_author(author_id)

        result = [Domain_to_Schema(course) for course in courses]

        return GenericResponse(
            success=True,
            message="Cursos encontrados exitosamente",
            data=result
        )
    except User_NotFound_Error as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/")
def all_courses(service: CourseService = Depends(get_course_service)):
    try:
        courses = service.find_courses()

        result = [Domain_to_Schema(course) for course in courses]

        return GenericResponse(
            success=True,
            message="Cursos encontrados exitosamente",
            data=result
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================ UPDATE ============================================
@router.patch("/{course_id}")
def course_update(course_id: int, course_data: CourseUpdate, service: CourseService = Depends(get_course_service), current_user: User = Depends(get_current_user)):
    try:
        # Conversion Schema -> Domain
        course_to_update = service.update_course(
            course_id=course_id,
            user_id=current_user.id,
            title=course_data.title,
            description=course_data.description
        )

        # Conversion Domain -> Schema
        result = Domain_to_Schema(course_to_update)

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
@router.delete("/{course_id}")
def course_delete(course_id: int, service: CourseService = Depends(get_course_service), current_user: User = Depends(get_current_user)):
    try:
        service.delete_course(course_id, current_user.id)

        return GenericResponse(
            success=True,
            message="Curso eliminado exitosamente",
            data=None
        )
    except Course_NotFound_Error as e:
        raise HTTPException(status_code=404, detail=str(e))
    except AccessDenied_Error as e:
        raise HTTPException(status_code=403, detail=str(e))
