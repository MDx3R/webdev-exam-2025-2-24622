from dataclasses import dataclass


@dataclass
class Role:
    """
    Entity representing a user role.
    """

    role_id: int
    name: str
    description: str

    def __post_init__(self):
        assert self.name, "Role name is required."
        assert self.description, "Role description is required."
