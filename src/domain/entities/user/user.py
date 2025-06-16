from dataclasses import dataclass

from domain.entities.entity import Entity, Id
from domain.entities.user.value_objects import FullName

from .role import Role


@dataclass
class User(Entity):
    """
    Aggregate root for User.
    """

    username: str
    password_hash: str
    full_name: FullName
    role: Role

    def __post_init__(self):
        assert self.username, "Username is required."
        assert self.password_hash, "Password hash is required."

    @property
    def user_id(self) -> Id | None:
        return self.id

    @classmethod
    def create(
        cls,
        username: str,
        password_hash: str,
        full_name: FullName,
        role: Role,
    ) -> "User":
        return cls(
            entity_id=None,
            username=username,
            password_hash=password_hash,
            full_name=full_name,
            role=role,
        )
