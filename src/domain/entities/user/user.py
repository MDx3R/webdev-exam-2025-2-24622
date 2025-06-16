from dataclasses import dataclass

from .role import Role


@dataclass
class User:
    """
    Aggregate root for User.
    """

    user_id: int
    username: str
    password_hash: str
    last_name: str
    first_name: str
    patronymic: str | None
    role: Role

    def __post_init__(self):
        assert self.username, "Username is required."
        assert self.password_hash, "Password hash is required."
        assert self.last_name, "Last name is required."
        assert self.first_name, "First name is required."
        if self.patronymic is not None:
            assert (
                self.patronymic.strip()
            ), "Patronymic must be non-empty or None."
