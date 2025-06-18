class ApplicationError(Exception):
    """Базовое исключение для всего приложения"""

    def __init__(
        self, message: str | None = None, *, cause: Exception | None = None
    ):
        super().__init__(message)
        self.message = message
        self.cause = cause

    def __str__(self):
        base = self.message or self.__class__.__name__
        if self.__cause__:
            return f"{base} (caused by {self.__cause__.__class__.__name__}: {self.__cause__})"
        return base


class RepositoryError(ApplicationError):
    """
    Базовое исключение для ошибок репозитория.
    """


class IntegrityError(RepositoryError):
    def __init__(self, message: str = "Нарушение целостности данных"):
        super().__init__(message)


class DuplicateEntryError(RepositoryError):
    def __init__(self, field: str, value: str):
        self.field = field
        self.value = value
        super().__init__(
            f"Дублирующая запись для поля '{field}': {value} уже существует"
        )


class InvalidCredentialsError(ApplicationError):
    def __init__(self, message: str):
        super().__init__(message)


class NotFoundError(ApplicationError):
    def __init__(self, id: int | str, entity: str):
        super().__init__(f"{entity.capitalize()} with ID {id} not found")
