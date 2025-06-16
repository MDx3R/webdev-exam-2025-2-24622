from abc import ABC, abstractmethod

from domain.entities.user import User


class UserRepository(ABC):
    """
    Interface for User aggregate repository.
    """

    @abstractmethod
    async def get_by_id(self, user_id: int) -> User: ...
    @abstractmethod
    async def get_by_username(self, username: str) -> User: ...
    @abstractmethod
    async def exists_by_username(self, username: str) -> User: ...
    @abstractmethod
    async def save(self, user: User) -> None: ...
