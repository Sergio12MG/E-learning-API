from src.main.application.validators.course_validators import Course_Return_Validator, Course_Existence_Validator
from src.main.application.validators.user_validators import UserBasicValidator
from src.main.domain.exceptions import AccessDenied_Error
from src.main.domain.models.course import Course
from src.main.domain.output_ports.course_ports import CourseRepository
from src.main.domain.output_ports.user_ports import UserRepository

class CourseService:
    def __init__(self, repository: CourseRepository, user_repo: UserRepository):
        self.repository = repository
        self.user_repo = user_repo
        self.return_validator = Course_Return_Validator(repository)
        self.exist_validator = Course_Existence_Validator(repository)
        self.user_validator = UserBasicValidator(user_repo)

    # ========= CREATE =========
    def create_course(self, title: str, description: str, user_id: int) -> Course:
        # 1. Data checks
        self.exist_validator.find_title(title)
        user = self.user_validator.find_id(user_id)
        
        # 2. Packaging of variables
        course = Course(id=0, title=title, description=description, user_id=user.id)

        return self.repository.save(course)
    
    # ========= READ =========
    def find_course_id(self, course_id: int) -> Course | None:
        return self.return_validator.find_by_id(course_id)
    
    def find_course_title(self, title: str) -> Course | None:
        return self.return_validator.find_by_title(title)
    
    # ========= UPDATE =========
    def update_course(self, course_id: int, user_id: int, title: str | None = None, description: str | None = None) -> Course:
        # 1. Check of existence of the course and the user
        current_course = self.return_validator.find_id(course_id)
        self.user_validator.check_course_owner(user_id, current_course.user_id)
        
        # 3. Prepare data to update
        final_title = title if title is not None else current_course.title
        final_description = description if description is not None else current_course.description

        # 4. Packaging of variables
        course_to_update = Course(
            id=current_course.id,
            title=final_title,
            description=final_description,
            user_id=current_course.user_id
        )

        return self.repository.update(course_to_update)

    # ========= DELETE =========
    def delete_course(self, course_id: int, user_id: int) -> None:
        current_course = self.return_validator.find_id(course_id)
        self.user_validator.check_course_owner(user_id, current_course.user_id)

        return self.repository.delete_id(current_course.id)
