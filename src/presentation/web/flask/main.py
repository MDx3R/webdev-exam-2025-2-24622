from collections.abc import Callable

from flask import Flask, session
from flask_login import (  # type: ignore
    LoginManager,
    UserMixin,
    logout_user,
)

from application.dtos.user.user_descriptor import UserDescriptor
from domain.repositories.user_repository import IUserRepository


login_manager = LoginManager()


class FlaskUserDescriptor(UserDescriptor, UserMixin):
    def get_id(self) -> str:
        return str(self.user_id)


class FlaskLoginManager(LoginManager):
    def __init__(
        self,
        user_repo: IUserRepository,
    ):
        super().__init__()  # type: ignore
        self.user_repo = user_repo
        self.set_user_loader(self.load_user)

    def configure(self, app: Flask, add_context_processor: bool = True):
        self.init_app(app, add_context_processor)  # type: ignore

    def set_user_loader(
        self, loader: Callable[[str], FlaskUserDescriptor | None]
    ):
        self.user_loader(loader)  # type: ignore

    def set_login_view(self, view_name: str):
        self.login_view = view_name

    def set_login_message(self, login_message: str):
        self.login_message = login_message

    def set_login_message_category(self, category: str):
        self.login_message_category = category

    def load_user(self, user_id: str) -> FlaskUserDescriptor | None:
        try:
            user = self.user_repo.get_by_id(int(user_id))
            return FlaskUserDescriptor(int(user_id), user.username, user.role)
        except Exception:
            # Защита от падения при некорректном user_id и др. ошибках
            session.clear()
            logout_user()

        return None
