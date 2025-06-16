from dataclasses import dataclass

from domain.entities.user.role import Role


@dataclass(frozen=True)
class UserDescriptor:
    user_id: int
    username: str
    role: Role
