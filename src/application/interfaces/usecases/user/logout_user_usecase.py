from abc import ABC, abstractmethod

from application.dtos.user.user_descriptor import UserDescriptor


class ILogoutUserUseCase(ABC):
    @abstractmethod
    def execute(self, descriptor: UserDescriptor) -> None: ...
