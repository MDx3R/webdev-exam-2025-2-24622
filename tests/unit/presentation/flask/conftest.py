import pytest
from flask_login import FlaskLoginClient  # type: ignore

from di.container import Container
from infrastructure.config.config import BASE_FILE_DIR, AuthConfig
from infrastructure.server.flask.app import FlaskServer


@pytest.fixture(scope="session")
def container():
    container = Container()
    container.init_resources()
    return container


@pytest.fixture(scope="session")
def auth_config():
    return AuthConfig(SECRET_KEY="secret-key")


@pytest.fixture(scope="session")
def server(container: Container, auth_config: AuthConfig):
    server = FlaskServer(BASE_FILE_DIR, container, auth_config)
    server.configure()
    server.setup_routes()
    return server


@pytest.fixture(scope="session")
def app(server: FlaskServer):
    app = server.app
    app.testing = True
    app.config["WTF_CSRF_ENABLED"] = False
    app.test_client_class = FlaskLoginClient
    return app
