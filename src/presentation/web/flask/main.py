from flask import Flask, session
from flask_login import (  # type: ignore
    LoginManager,
    UserMixin,
    current_user,
    logout_user,
)

from application.dtos.user.user_descriptor import UserDescriptor
from domain.repositories.user_repository import IUserRepository


login_manager = LoginManager()


class FlaskUserDescriptor(UserDescriptor, UserMixin):
    def get_id(self) -> str:
        return str(self.user_id)


def get_current_user() -> FlaskUserDescriptor:
    return current_user  # type: ignore


def init_login_manager(app: Flask, user_repo: IUserRepository):
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"  # type: ignore
    login_manager.login_message = "Для доступа к данной странице необходимо пройти процедуру аутентификации."
    login_manager.login_message_category = "warning"

    def load_user(user_id: str) -> FlaskUserDescriptor | None:
        try:
            user = user_repo.get_by_id(int(user_id))
            return FlaskUserDescriptor(int(user_id), user.username, user.role)
        except Exception:
            # Защита от падения при некорректном user_id и др. ошибках
            session.clear()
            logout_user()

        return None

    login_manager.user_loader(load_user)  # type: ignore
    login_manager.init_app(app)  # type: ignore
