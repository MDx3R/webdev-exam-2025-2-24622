from flask import Flask
from flask_login import LoginManager, UserMixin, current_user  # type: ignore

from application.dtos.user.user_descriptor import UserDescriptor
from domain.repositories.user_repository import IUserRepository


login_manager = LoginManager()


class FlaskUserDescriptor(UserDescriptor, UserMixin):
    pass


def get_current_user() -> FlaskUserDescriptor:
    return current_user  # type: ignore


def init_login_manager(app: Flask, user_repo: IUserRepository):
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"  # type: ignore
    login_manager.login_message = "Для доступа к данной странице необходимо пройти процедуру аутентификации."
    login_manager.login_message_category = "warning"

    def load_user(user_id: int) -> FlaskUserDescriptor:
        user = user_repo.get_by_id(user_id)
        return FlaskUserDescriptor(user_id, user.username, user.role)

    login_manager.user_loader(load_user)  # type: ignore
    login_manager.init_app(app)  # type: ignore
