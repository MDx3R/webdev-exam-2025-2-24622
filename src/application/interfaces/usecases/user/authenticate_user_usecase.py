from abc import ABC, abstractmethod

from application.dtos.user.user_dto import UserDTO


class IAuthenticateUserUseCase(ABC):
    @abstractmethod
    def execute(self, username: str, password: str) -> UserDTO: ...
