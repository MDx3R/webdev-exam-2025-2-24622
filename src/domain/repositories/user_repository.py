from abc import ABC, abstractmethod

from domain.entities.user import User


class IUserRepository(ABC):
    """
    Interface for User aggregate repository.
    """

    @abstractmethod
    def get_by_id(self, user_id: int) -> User: ...
    @abstractmethod
    def get_by_username(self, username: str) -> User: ...
    @abstractmethod
    def exists_by_username(self, username: str) -> bool: ...
    @abstractmethod
    def save(self, user: User) -> User: ...
