from application.dtos.user.user_descriptor import UserDescriptor
from application.interfaces.usecases.user.logout_user_usecase import (
    ILogoutUserUseCase,
)


class LogoutUserUseCase(ILogoutUserUseCase):
    def __init__(self):
        pass

    def execute(self, descriptor: UserDescriptor) -> None:
        pass  # Handled by session management in infrastructure layer
