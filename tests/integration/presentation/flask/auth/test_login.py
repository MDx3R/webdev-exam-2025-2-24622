import pytest
from flask import Flask

from di.container import Container
from presentation.web.flask.main import FlaskUserDescriptor


class TestLogin:
    @pytest.fixture(autouse=True)
    def setup(
        self,
        flask_app: Flask,
        container: Container,
        user_descriptor: FlaskUserDescriptor,
    ):
        self.app = flask_app
        self.container = container
        self.user = user_descriptor
        self.client = flask_app.test_client()
        self.logged_in_client = flask_app.test_client(user=self.user)
        yield

    def test_login(self):
        response = self.client.post(
            "/auth/login",
            data={
                "username": self.user.username,
                "password": "testpass",
            },
            follow_redirects=True,
        )

        cookie_value = self.client.get_cookie("session")
        assert cookie_value is not None
        assert "Logged in." in response.text

    def test_login_raises_when_invalid_username(self):
        response = self.client.post(
            "/auth/login",
            data={
                "username": "invaliduser",
                "password": "invalidpass",
            },
            follow_redirects=True,
        )

        assert (
            "User with username invaliduser does not exist." in response.text
        )

    def test_login_raises_when_invalid_pass(self):
        response = self.client.post(
            "/auth/login",
            data={
                "username": self.user.username,
                "password": "invalidpass",
            },
            follow_redirects=True,
        )

        assert "Invalid credentials." in response.text

    def test_login_redirects_when_authenticated(self):
        response = self.logged_in_client.get("/auth/login")
        assert response.headers.get("Location") == "/"

    def test_logout(self):
        response = self.logged_in_client.post(
            "/auth/logout",
            follow_redirects=True,
        )

        cookie_value = self.client.get_cookie("session")
        assert cookie_value is None
        assert "Logged out." in response.text

    def test_logout_redirects_when_not_authenticated(self):
        response = self.client.post("/auth/logout")

        loc = response.headers.get("Location")
        assert loc
        assert "/auth/login" in loc
