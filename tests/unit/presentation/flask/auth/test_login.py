from unittest.mock import Mock

import pytest
from dependency_injector import providers
from flask import Flask

from application.dtos.user.user_dto import UserDTO
from application.exceptions import InvalidCredentialsError
from application.interfaces.usecases.user.authenticate_user_usecase import (
    IAuthenticateUserUseCase,
)
from application.interfaces.usecases.user.logout_user_usecase import (
    ILogoutUserUseCase,
)
from domain.entities.user.role import RoleEnum
from presentation.web.flask.main import FlaskUserDescriptor
from tests.unit.presentation.flask.conftest import Container


class TestLogin:
    @pytest.fixture(autouse=True)
    def setup(self, app: Flask, container: Container):
        self.app = app
        self.container = container
        self.client = app.test_client()
        self.user = FlaskUserDescriptor(1, "username", RoleEnum.ADMIN.value)
        self.logged_in_client = app.test_client(user=self.user)
        yield

    def mock_auth_us(
        self, output: UserDTO | None = None, raises: Exception | None = None
    ):
        mock = Mock(spec=IAuthenticateUserUseCase)
        if output:
            mock.execute.return_value = output
        mock.execute.side_effect = raises

        self.container.override_providers(auth_uc=providers.Object(mock))

    def test_login(self):
        user = UserDTO(1, "user", "surname", "name", "patronymic", "user")
        self.mock_auth_us(user)

        response = self.client.post(
            "/auth/login",
            data={
                "username": "user",
                "password": "testpass",
            },
            follow_redirects=True,
        )

        assert "Logged in." in response.text

    def test_login_raises_when_invalid(self):
        self.mock_auth_us(
            raises=InvalidCredentialsError("Invalid credentials")
        )

        response = self.client.post(
            "/auth/login",
            data={
                "username": "user",
                "password": "invalidpass",
            },
            follow_redirects=True,
        )

        assert "Invalid credentials." in response.text

    def test_login_shows_exception(self):
        self.mock_auth_us(raises=Exception("Some exception"))

        response = self.client.post(
            "/auth/login",
            data={
                "username": "user",
                "password": "invalidpass",
            },
            follow_redirects=True,
        )

        assert "Some exception" in response.text

    def test_login_redirects_when_authenticated(self):
        response = self.logged_in_client.get("/auth/login")
        assert response.headers.get("Location") == "/"

    def mock_logout_us(self, raises: Exception | None = None):
        mock = Mock(spec=ILogoutUserUseCase)
        mock.execute.side_effect = raises
        self.container.override_providers(logout_uc=providers.Object(mock))

    def test_logout(self):
        self.mock_logout_us()

        response = self.logged_in_client.post(
            "/auth/logout",
            follow_redirects=True,
        )

        assert "Logged out." in response.text

    def test_logout_shows_exception(self):
        self.mock_logout_us(Exception("Some exception"))

        response = self.logged_in_client.post(
            "/auth/logout",
            follow_redirects=True,
        )

        assert "Some exception" in response.text

    def test_logout_redirects_when_not_authenticated(self):
        response = self.client.post("/auth/logout")

        loc = response.headers.get("Location")
        assert loc
        assert "/auth/login" in loc
