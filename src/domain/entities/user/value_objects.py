from dataclasses import dataclass


@dataclass(frozen=True)
class FullName:
    surname: str
    name: str
    patronymic: str | None

    def __post_init__(self):
        assert (
            self.patronymic and not self.patronymic.strip()
        ), "Patronymic must be None or non-empty string"

        assert (
            self.surname.strip() and self.name.strip()
        ), "Surname and name must not be empty"

    def short(self) -> str:
        return f"{self.surname} {self.name[0]}."

    def full(self) -> str:
        return f"{self.surname} {self.name} {self.patronymic or ''}".strip()

    @staticmethod
    def create(surname: str, name: str, patronymic: str | None) -> "FullName":
        return FullName(
            surname=surname.strip(),
            name=name.strip(),
            patronymic=patronymic.strip() if patronymic else None,
        )
