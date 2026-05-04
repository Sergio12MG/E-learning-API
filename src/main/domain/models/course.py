from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Topic:
    id: int
    title: str
    module_id: int
    content: Optional[str] = None
    order: int = 0
    topic_type: str = "text"
    resource_url: Optional[str] = None

@dataclass
class CModule:
    id: int
    title: str
    course_id: int
    is_published: bool
    order: int = 0
    description: Optional[str] = None
    parent_id: Optional[int] = None

    # Tree structure
    submodules: List['CModule'] = field(default_factory=list)
    topics: List[Topic] = field(default_factory=list)

    def add_submodules(self, submodule: 'CModule') -> None:
        """Add a child submodule"""
        submodule.parent_id = self.id
        self.submodules.append(submodule)

    def add_topic(self, topic: Topic) -> None:
        """Add a topic to the module"""
        self.topics.append(topic)

    def get_all_submodules(self) -> List['CModule']:
        """Get all the submodules recursively"""
        all_submodules = self.submodules.copy()

        for submodule in self.submodules:
            all_submodules.extend(submodule.get_all_submodules())

        return all_submodules

    def get_all_topics(self) -> List[Topic]:
        """Get all the topics recursively (current + submodules)"""
        all_topics = self.topics.copy()

        for submodule in self.submodules:
            all_topics.extend(submodule.get_all_topics())

        return all_topics
    
@dataclass
class Course:
    id: int
    title: str
    user_id: int
    description: Optional[str] = None
    modules: List[CModule] = field(default_factory=list)

    def add_module(self, module: CModule) -> None:
        """Add a root module to the course"""
        module.course_id = self.id
        self.modules.append(module)
