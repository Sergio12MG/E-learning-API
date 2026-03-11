from abc import ABC, abstractmethod
from src.main.domain.models.course import Course
from src.main.domain.output_ports.course_ports import CourseRepository
from src.main.domain.exceptions import Course_NotFound_Error, Course_TitleRepeated_Error

class Course_Validator(ABC):
    @abstractmethod
    def find_title(self, title: str):
        pass

class Course_Return_Validator(Course_Validator):
    def __init__(self, repository: CourseRepository):
        self.repository = repository

    def find_id(self, course_id: int):
        course = self.repository.find_by_id(course_id)

        if course is None:
            raise Course_NotFound_Error(f"No existe un curso con el ID {course_id}.")
        
        return course
    
    def find_title(self, title: str):
        course = self.repository.find_by_title(title)

        if course is None:
            raise Course_NotFound_Error(f"No se ha encontrado un curso llamado '{title}'.")
        
        return course
    
class Course_Existence_Validator(Course_Validator):
    def __init__(self, repository: CourseRepository):
        self.repository = repository
        
    def find_title(self, title: str):
        if self.repository.find_by_title(title):
            raise Course_TitleRepeated_Error(f"Ya existe un curso con el mismo título ('{title}').")
        return
