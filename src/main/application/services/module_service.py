from typing import List

from src.main.domain.models.course import CModule
from src.main.domain.output_ports.module_ports import ModuleRepository
from src.main.domain.output_ports.course_ports import CourseRepository
from src.main.domain.output_ports.user_ports import UserRepository
from src.main.application.validators.module_validators import Module_Validator
from src.main.application.validators.course_validators import Course_Return_Validator
from src.main.application.validators.user_validators import UserBasicValidator

class ModuleService:
    def __init__(self, repository: ModuleRepository, course_repo: CourseRepository, user_repo: UserRepository):
        self.repository = repository
        self.course_repo = course_repo
        self.user_repo = user_repo
        self.module_validator = Module_Validator(repository)
        self.course_validator = Course_Return_Validator(course_repo)
        self.user_validator = UserBasicValidator(user_repo)
    
    # ========= CREATE =========
    def create_module(self, title: str, course_id: int, order: int, is_published: bool, description: str | None = None, parent_id: int | None = None) -> CModule:
        # 1. Data checks
        course = self.course_validator.find_id(course_id)
        if parent_id:
            parent = self.module_validator.check_parent_module(parent_id)

        # 2. Packaging of variables
        module = CModule(
            id=0,
            title=title,
            course_id=course_id,
            order=order,
            is_published=is_published,
            description=description,
            parent_id=parent_id
        )

        return self.repository.save(module)
    
    # ========= READ =========
    def find_module_id(self, module_id: int) -> CModule | None:
        return self.module_validator.find_id(module_id)
    
    def find_module_title(self, title: str) -> CModule | None:
        return self.module_validator.find_title(title)
    
    def find_child_modules(self, parent_id: int) -> List[CModule] | None:
        return self.repository.find_submodules(parent_id)
    
    # ========= UPDATE =========
    def update_module(self,
        module_id: int | None = None,
        title: str | None = None,
        order: int | None = None,
        is_published: bool | None = None,
        description: str | None = None,
        new_parent_id: int | None = None
        ) -> CModule:
        # 1. Data checks
        current_module = self.module_validator.find_id(module_id)

        # 2. Prepare data to update
        final_title = title if title is not None else current_module.title
        final_order = order if order is not None else current_module.order
        final_published_state = is_published if is_published is not None else current_module.is_published
        final_description = description if description is not None else current_module.description

        # Parent module allocation handler
        final_parent = None
        if new_parent_id is not None:
            parent = self.module_validator.check_parent_module(new_parent_id)
            if parent.id != current_module.parent_id:
                final_parent = new_parent_id
        else:
            final_parent = current_module.parent_id

        # 3. Packaging of variables
        module_to_update = CModule(
            id=module_id,
            title=final_title,
            course_id=current_module.course_id,
            order=final_order,
            is_published=final_published_state,
            description=final_description,
            parent_id=final_parent
        )

        return self.repository.update(module_to_update)
    
    def delete_module(self, module_id: int, user_id: int) -> None:
        # 1. Checks the module exists
        current_module = self.module_validator.find_id(module_id)
        # 2. Obtains the course to which it belongs
        course = self.course_validator.find_id(current_module.course_id)
        # 3. Verify the user owns the course
        self.user_validator.check_course_owner(user_id, course.user_id)

        return self.repository.delete_id(current_module.id)
