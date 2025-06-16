from dataclasses import dataclass


@dataclass
class UserDTO:
    id: int
    username: str
    surname: str
    name: str
    patronymic: str | None
    role: str
