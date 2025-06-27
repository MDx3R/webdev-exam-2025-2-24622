from typing import Any

import pytest
from flask_login import FlaskLoginClient  # type: ignore
from sqlalchemy import insert

from di.container import Container
from domain.entities.user.role import RoleEnum
from infrastructure.app.app import App
from infrastructure.sqlalchemy.initializer.role_seeder import seed_roles
from infrastructure.sqlalchemy.models.base import Base
from infrastructure.sqlalchemy.models.user import UserModel
from presentation.web.flask.main import FlaskUserDescriptor


@pytest.fixture(scope="session")
def app():
    app = App()
    app.configure()
    yield app
    app.shutdown()


@pytest.fixture(scope="session")
def container(app: App):
    return app.container


@pytest.fixture(scope="session")
def admin_data(container: Container) -> dict[str, Any]:
    return {
        "id": 1,
        "username": "admin",
        "password_hash": container.password_hasher().hash("testpass"),
        "surname": "doe",
        "name": "john",
        "patronymic": "first",
        "role_id": RoleEnum.ADMIN.value.id_safe.value,
    }


@pytest.fixture(scope="session")
def user_data(container: Container) -> dict[str, Any]:
    return {
        "id": 2,
        "username": "user",
        "password_hash": container.password_hasher().hash("testpass"),
        "surname": "doe",
        "name": "jane",
        "patronymic": None,
        "role_id": RoleEnum.USER.value.id_safe.value,
    }


@pytest.fixture(scope="session")
def third_user_data(container: Container) -> dict[str, Any]:
    return {
        "id": 3,
        "username": "jack",
        "password_hash": container.password_hasher().hash("testpass"),
        "surname": "doe",
        "name": "jack",
        "patronymic": None,
        "role_id": RoleEnum.USER.value.id_safe.value,
    }


@pytest.fixture(scope="session")
def users_data(
    admin_data: dict[str, Any], user_data: dict[str, Any]
) -> list[dict[str, Any]]:
    return [admin_data, user_data]


@pytest.fixture(scope="session", autouse=True)
def setup_database(container: Container):
    database = container.database()
    Base.metadata.create_all(database.engine)
    session = container.database().get_session_factory()()
    seed_roles(session)
    session.close()
    yield
    Base.metadata.drop_all(database.engine)


@pytest.fixture(autouse=True)
def clean_and_seed(container: Container, users_data: list[dict[str, Any]]):
    session = container.database().get_session_factory()()

    for table in reversed(Base.metadata.sorted_tables):
        if table.name == "Roles":
            continue
        session.execute(table.delete())

    stmt = insert(UserModel)
    session.execute(stmt, users_data)
    session.commit()

    yield
    session.close()


@pytest.fixture(scope="session")
def flask_app(app: App):
    server = app.get_server()
    server.testing = True
    server.config["WTF_CSRF_ENABLED"] = False
    server.test_client_class = FlaskLoginClient
    return server


@pytest.fixture(scope="session")
def admin_descriptor():
    return FlaskUserDescriptor(
        1, "admin", RoleEnum.ADMIN.value  # type: ignore
    )


@pytest.fixture(scope="session")
def user_descriptor():
    return FlaskUserDescriptor(2, "user", RoleEnum.USER.value)  # type: ignore


@pytest.fixture()
def third_user_descriptor(
    container: Container, third_user_data: dict[str, Any]
):
    session = container.database().get_session_factory()()
    stmt = insert(UserModel)
    session.execute(stmt, [third_user_data])
    session.commit()
    session.close()
    return FlaskUserDescriptor(3, "jack", RoleEnum.USER.value)  # type: ignore
