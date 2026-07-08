from typing import List

from src.main.application.validators.course_validators import Course_Return_Validator
from src.main.domain.models.course import Topic
from src.main.domain.output_ports.topic_ports import TopicRepository
from src.main.domain.output_ports.module_ports import ModuleRepository
from src.main.domain.output_ports.course_ports import CourseRepository
from src.main.domain.output_ports.user_ports import UserRepository
from src.main.application.validators.topic_validators import Topic_Validator
from src.main.application.validators.module_validators import Module_Validator
from src.main.application.validators.user_validators import UserBasicValidator

class TopicService:
    def __init__(self, repository: TopicRepository, module_repo: ModuleRepository, course_repo: CourseRepository, user_repo: UserRepository):
        self.repository = repository
        self.module_repo = module_repo
        self.course_repo = course_repo
        self.user_repo = user_repo
        self.topic_validator = Topic_Validator(repository)
        self.module_validator = Module_Validator(module_repo)
        self.course_validator = Course_Return_Validator(course_repo)
        self.user_validator = UserBasicValidator(user_repo)

    # ========= CREATE =========
    def create_topic(self, title: str, module_id: int, content: str | None = None, resource_url: str | None = None, order: int = 0, topic_type: str = "text") -> Topic:
        # Check if the module exists
        module = self.module_validator.find_id(module_id)
        
        topic = Topic(
            id=0,
            title=title,
            content=content,
            order=order,
            topic_type=topic_type,
            resource_url=resource_url,
            module_id=module_id
        )

        return self.repository.save(topic)
    
    # ========= READ =========
    # By ID
    def find_topic_id(self, topic_id: int) -> Topic | None:
        return self.topic_validator.find_id(topic_id)

    # By title
    def find_topic_title(self, title: str) -> Topic | None:
        return self.topic_validator.find_title(title)

    # By the module that contains them
    def find_all_topics(self, module_id: int) -> List[Topic] | None:
        # 1. Checks that the module exists
        module = self.module_validator.find_id(module_id)
        # 2. Find all the topics inside the module
        topics = self.repository.find_all_by_module(module_id)

        # 3. Add each topic to the array
        module.add_topic([topic for topic in topics])
        
        return topics
    
    # ========= UPDATE =========
    def update_topic(self,
        topic_id: int,
        title: str | None = None,
        content: str | None = None,
        order: int | None = None,
        topic_type: str | None = None,
        resource_url: str | None = None,
        ) -> Topic:
        # 1. Data checks
        current_topic = self.topic_validator.find_id(topic_id)

        # 2. Prepare data to update
        final_title = title if title is not None else current_topic.title
        final_content = content if content is not None else current_topic.content
        final_order = order if order is not None else current_topic.order
        final_topic_type = topic_type if topic_type is not None else current_topic.topic_type
        final_resource_url = resource_url if resource_url is not None else current_topic.resource_url

        # 3. Packaging of varaibles
        topic_to_update = Topic(
            id=topic_id,
            title=final_title,
            content=final_content,
            order=final_order,
            topic_type=final_topic_type,
            resource_url=final_resource_url,
            module_id=current_topic.module_id
        )

        return self.repository.update(topic_to_update)
    
    # ========= DELETE =========
    def delete_topic(self, topic_id: int) -> None:
        # 1. Verify the topic exists
        current_topic = self.topic_validator.find_id(topic_id)

        return self.repository.delete_id(current_topic.id)
