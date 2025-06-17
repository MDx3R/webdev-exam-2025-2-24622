from dataclasses import dataclass
from typing import Self

from domain.entities.user.user import User


@dataclass
class UserDTO:
    id: int
    username: str
    surname: str
    name: str
    patronymic: str | None
    role: str

    @classmethod
    def from_domain(cls, user: User) -> Self:
        return cls(
            id=user.id_safe.value,
            username=user.username,
            surname=user.full_name.surname,
            name=user.full_name.name,
            patronymic=user.full_name.patronymic,
            role=user.role.name,
        )
