from dataclasses import dataclass
from typing import Self

from domain.entities.user.role import Role
from domain.entities.user.user import User


@dataclass(frozen=True)
class UserDescriptor:
    user_id: int
    username: str
    role: Role

    @classmethod
    def from_domain(cls, user: User) -> Self:
        return cls(
            user_id=user.id_safe.value,
            username=user.username,
            role=user.role,
        )
