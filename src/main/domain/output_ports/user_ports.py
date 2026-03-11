from abc import ABC, abstractmethod
from src.main.domain.models.user import User

class UserRepository(ABC):
    @abstractmethod
    def save(self, user: User) -> User:
        pass

    @abstractmethod
    def find_by_id(self, user_id: int) -> User | None:
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> User | None:
        pass

    @abstractmethod
    def update(self, user: User) -> User | None:
        pass

    @abstractmethod
    def delete_id(self, user_id: int) -> None:
        pass
