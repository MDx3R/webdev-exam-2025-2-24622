from abc import ABC, abstractmethod

from domain.entities.user.dtos import UserData
from domain.entities.user.user import User
from domain.entities.user.value_objects import FullName


class IUserFactory(ABC):
    @abstractmethod
    def create(self, data: UserData) -> User: ...


class UserFactory(IUserFactory):
    def create(self, data: UserData) -> User:
        return User(
            entity_id=None,
            username=data.username,
            password_hash=data.password_hash,
            full_name=FullName.create(
                surname=data.surname,
                name=data.name,
                patronymic=data.patronymic,
            ),
            role=data.role,
        )
