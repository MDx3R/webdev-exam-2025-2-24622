from dataclasses import dataclass
from enum import Enum

from domain.entities.entity import Entity, Id


@dataclass
class Role(Entity):
    """
    Entity representing a user role.
    """

    name: str
    description: str

    def __post_init__(self):
        assert self.name.strip(), "Role name is required."
        assert self.description.strip(), "Role description is required."

    @property
    def role_id(self) -> Id | None:
        return self.id

    @classmethod
    def create(
        cls,
        name: str,
        description: str,
    ) -> "Role":
        return cls(
            entity_id=None,
            name=name,
            description=description,
        )


class RoleEnum(Enum):
    """
    Entity representing a user role.
    """

    ADMIN = Role(
        entity_id=Id(1),
        name="Администратор",
        description="Суперпользователь, имеет полный доступ к системе, в том числе к редактированию и удалению рецептов и отзывов пользователей",
    )
    USER = Role(
        entity_id=Id(2),
        name="Пользователь",
        description="Может добавлять рецепты и отзывы, редактировать и удалять только свои рецепты и отзывы",
    )
