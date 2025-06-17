from application.dtos.user.user_dto import UserDTO
from application.exceptions import InvalidCredentialsError
from application.interfaces.services.password_hash_service import (
    IPasswordHasher,
)
from application.interfaces.usecases.user.authenticate_user_usecase import (
    IAuthenticateUserUseCase,
)
from domain.repositories.user_repository import IUserRepository


class AuthenticateUserUseCase(IAuthenticateUserUseCase):
    def __init__(
        self,
        user_repository: IUserRepository,
        password_hasher: IPasswordHasher,
    ):
        self.user_repository = user_repository
        self.password_hasher = password_hasher

    def execute(self, username: str, password: str) -> UserDTO:
        user = self.user_repository.get_by_username(username)
        if not user:
            raise InvalidCredentialsError("Invalid username")

        if not self.password_hasher.verify(password, user.password_hash):
            raise InvalidCredentialsError("Invalid password")

        return UserDTO(
            id=user.id_safe.value,
            username=user.username,
            surname=user.full_name.surname,
            name=user.full_name.name,
            patronymic=user.full_name.patronymic,
            role=user.role.name,
        )
