from abc import ABC, abstractmethod
from typing import List

from src.main.domain.models.course import CModule, Topic

class ModuleRepository(ABC):
    @abstractmethod
    def save(self, module: CModule) -> CModule:
        pass

    @abstractmethod
    def find_by_id(self, module_id: int) -> CModule | None:
        pass

    @abstractmethod
    def find_by_title(self, title: str) -> CModule | None:
        pass

    @abstractmethod
    def find_submodules(self, parent_id: int) -> List[CModule] | None:
        pass

    @abstractmethod
    def find_topics(self, module_id: int) -> Topic | None:
        pass

    @abstractmethod
    def update(self, module: CModule) -> CModule | None:
        pass

    @abstractmethod
    def delete_id(self, module_id: int) -> None:
        pass
