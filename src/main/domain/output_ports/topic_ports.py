from abc import ABC, abstractmethod
from typing import List
from src.main.domain.models.course import Topic

class TopicRepository(ABC):
    @abstractmethod
    def save(self, topic: Topic) -> Topic:
        pass

    @abstractmethod
    def find_by_id(self, topic_id: int) -> Topic | None:
        pass

    @abstractmethod
    def find_by_title(self, title: str) -> Topic | None:
        pass

    @abstractmethod
    def find_all_by_module(self, module_id: int) -> List[Topic] | None:
        pass

    @abstractmethod
    def update(self, topic: Topic) -> Topic | None:
        pass

    @abstractmethod
    def delete_id(self, topic_id: int) -> None:
        pass
