from abc import ABC, abstractmethod
from src.main.domain.models.course import Topic

class TopicRepository(ABC):
    @abstractmethod
    def save(self, topic: Topic) -> Topic:
        pass

    @abstractmethod
    def find_by_id(self, topic_id: int) -> Topic | None:
        pass

    @abstractmethod
    def update(self, topic: Topic) -> Topic | None:
        pass

    @abstractmethod
    def delete_id(self, topic_id: int) -> None:
        pass
