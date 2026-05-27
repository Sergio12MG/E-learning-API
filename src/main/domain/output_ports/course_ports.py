from abc import ABC, abstractmethod
from typing import List
from src.main.domain.models.course import Course

class CourseRepository(ABC):
    @abstractmethod
    def save(self, course: Course) -> Course:
        pass

    @abstractmethod
    def find_by_id(self, course_id: int) -> Course | None:
        pass

    @abstractmethod
    def find_by_title(self, title: str) -> Course | None:
        pass

    @abstractmethod
    def find_by_author(self, author_id: int) -> List[Course] | None:
        pass

    @abstractmethod
    def find_all(self) -> List[Course] | None:
        pass

    @abstractmethod
    def update(self, course: Course) -> Course | None:
        pass

    @abstractmethod
    def delete_id(self, course_id: int) -> None:
        pass
