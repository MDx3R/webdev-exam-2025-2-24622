import pytest

from application.dtos.user.user_descriptor import UserDescriptor
from application.usecases.user.logout_user_usecase import LogoutUserUseCase
from domain.entities.user.role import RoleEnum


class TestLogoutUserUseCase:
    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.use_case = LogoutUserUseCase()

    def setup_user(self, user_id: int = 10) -> UserDescriptor:
        return UserDescriptor(
            user_id=user_id, username="john_doe", role=RoleEnum.USER.value
        )

    def test_successful_logout(self) -> None:
        user = self.setup_user()
        self.use_case.execute(descriptor=user)
        assert True  # No-op without errors
