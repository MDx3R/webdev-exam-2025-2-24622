from dataclasses import dataclass

from domain.entities.user.role import Role


@dataclass(frozen=True)
class UserData:
    username: str
    password_hash: str
    surname: str
    name: str
    patronymic: str | None
    role: Role
