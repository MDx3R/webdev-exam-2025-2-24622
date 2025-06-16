from dataclasses import dataclass

from domain.entities.entity import Entity, Id


@dataclass
class Role(Entity):
    """
    Entity representing a user role.
    """

    name: str
    description: str

    def __post_init__(self):
        assert self.name, "Role name is required."
        assert self.description, "Role description is required."

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
