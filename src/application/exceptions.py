class ApplicationError(Exception):
    """Базовое исключение для всего приложения"""

    def __init__(self, message: str | None = None):
        self.message = message
        super().__init__(message)

    def __str__(self):
        return self.message or self.__class__.__name__


class InvalidCredentialsError(ApplicationError):
    def __init__(self, message: str):
        super().__init__(message)


class NotFoundError(ApplicationError):
    def __init__(self, id: int, entity: str):
        super().__init__(f"{entity.capitalize()} with ID {id} not found")
