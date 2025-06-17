# Tests for user use cases: AuthenticateUserUseCase, LogoutUserUseCase
from unittest.mock import Mock

import pytest

from application.dtos.user.user_dto import UserDTO
from application.exceptions import InvalidCredentialsError
from application.usecases.user.authenticate_user_usecase import (
    AuthenticateUserUseCase,
)
from domain.entities.entity import Id
from domain.entities.user.role import RoleEnum
from domain.entities.user.user import User
from domain.entities.user.value_objects import FullName


class TestAuthenticateUserUseCase:
    @pytest.fixture(autouse=True)
    def setup(
        self, mock_user_repository: Mock, mock_password_hasher: Mock
    ) -> None:
        self.mock_user_repository = mock_user_repository
        self.mock_password_hasher = mock_password_hasher
        self.use_case = AuthenticateUserUseCase(
            user_repository=self.mock_user_repository,
            password_hasher=self.mock_password_hasher,
        )

    def setup_user_entity(self, *, username: str = "user") -> User:
        user = User(
            entity_id=Id(1),
            username=username,
            full_name=FullName(surname="Doe", name="John", patronymic=None),
            password_hash="hash",
            role=RoleEnum.USER.value,
        )
        self.mock_user_repository.get_by_username.return_value = user
        return user

    def test_successful_authentication(self) -> None:
        password = "password"
        user = self.setup_user_entity()

        result = self.use_case.execute(
            username=user.username, password=password
        )

        assert isinstance(result, UserDTO)
        assert result.id == 1
        assert result.username == user.username
        assert result.surname == user.full_name.surname
        assert result.name == user.full_name.name
        assert result.patronymic is None
        assert result.role == RoleEnum.USER.value.name

        self.mock_user_repository.get_by_username.assert_called_once_with(
            user.username
        )
        self.mock_password_hasher.verify.assert_called_once_with(
            password, user.password_hash
        )

    def test_invalid_username_raises_error(self) -> None:
        self.mock_user_repository.get_by_username.return_value = None
        with pytest.raises(InvalidCredentialsError, match="Invalid username"):
            self.use_case.execute(
                username="unknown_user", password="password123"
            )
        self.mock_user_repository.get_by_username.assert_called_once_with(
            "unknown_user"
        )
        self.mock_password_hasher.verify.assert_not_called()

    def test_invalid_password_raises_error(self) -> None:
        user = self.setup_user_entity()
        self.mock_password_hasher.verify.return_value = False
        with pytest.raises(InvalidCredentialsError, match="Invalid password"):
            self.use_case.execute(
                username=user.username, password="wrong_password"
            )
        self.mock_user_repository.get_by_username.assert_called_once_with(
            user.username
        )
        self.mock_password_hasher.verify.assert_called_once_with(
            "wrong_password", user.password_hash
        )
