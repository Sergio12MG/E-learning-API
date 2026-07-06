from typing import List

from sqlalchemy.orm import Session

from src.main.domain.models.course import Course
from src.main.domain.output_ports.course_ports import CourseRepository
from src.main.infraestructure.db.models import Course as ORMCourse

class Entity_Converter:
    @staticmethod
    def Domain_to_ORM(domain: Course) -> ORMCourse:
        return ORMCourse(
            title=domain.title,
            description=domain.description,
            user_id=domain.user_id
        )
    
    @staticmethod
    def ORM_to_Domain(orm: ORMCourse) -> Course:
        return Course(
            id=orm.id,
            title=orm.title,
            description=orm.description,
            user_id=orm.user_id
        )

class SQLAlchemy_CourseRepository(CourseRepository):
    def __init__(self, db: Session):
        self.db = db

    # ========= CREATE =========
    def save(self, course: Course) -> Course:
        # Conversion Domain -> ORM
        orm_course = Entity_Converter.Domain_to_ORM(course)

        self.db.add(orm_course)
        self.db.commit()
        self.db.refresh(orm_course)

        # Conversion ORM -> Domain
        return Entity_Converter.ORM_to_Domain(orm_course)

    # ========= READ =========
    # By ID
    def find_by_id(self, course_id: int) -> Course | None:
        orm_course = self.db.get(ORMCourse, course_id)

        if not orm_course:
            return None
        
        return Entity_Converter.ORM_to_Domain(orm_course)
    
    # By title
    def find_by_title(self, title: str) -> Course | None:
        orm_course = self.db.query(ORMCourse).filter(ORMCourse.title == title).first()

        if orm_course:
            return Entity_Converter.ORM_to_Domain(orm_course)
        
        return None
    
    # By author
    def find_by_author(self, author_id: int) -> List[Course] | None:
        orm_courses = self.db.query(ORMCourse).filter(ORMCourse.user_id == author_id).all()

        return [Entity_Converter.ORM_to_Domain(orm_course) for orm_course in orm_courses]

    # All courses
    def find_all(self) -> List[Course] | None:
        orm_courses = self.db.query(ORMCourse).all()

        return [Entity_Converter.ORM_to_Domain(orm_course) for orm_course in orm_courses]
    
    # ========= UPDATE =========
    def update(self, course: Course) -> Course:
        orm_course = self.db.get(ORMCourse, course.id)

        if not orm_course:
            return None

        orm_course.title = course.title
        orm_course.description = course.description

        self.db.commit()
        self.db.refresh(orm_course)

        return Entity_Converter.ORM_to_Domain(orm_course)
    
    # ========= DELETE =========
    def delete_id(self, course_id: int) -> None:
        orm_course = self.db.get(ORMCourse, course_id)

        if orm_course:
            self.db.delete(orm_course)
            self.db.commit()

        return None
