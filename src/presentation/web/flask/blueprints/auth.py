from flask import (
    flash,
    redirect,
    render_template,
    url_for,
)
from flask.views import MethodView
from flask_login import (  # type: ignore
    current_user,
    login_required,  # type: ignore
    login_user,  # type: ignore
    logout_user,
)

from application.dtos.user.user_dto import UserDTO
from application.exceptions import InvalidCredentialsError, NotFoundError
from application.interfaces.usecases.user.authenticate_user_usecase import (
    IAuthenticateUserUseCase,
)
from application.interfaces.usecases.user.logout_user_usecase import (
    ILogoutUserUseCase,
)
from domain.entities.user.role import Role, RoleEnum
from presentation.web.flask.forms import LoginForm
from presentation.web.flask.main import FlaskUserDescriptor
from presentation.web.flask.utils import get_current_user


class LoginView(MethodView):
    admin_role = RoleEnum.ADMIN.value
    user_role = RoleEnum.USER.value

    def __init__(self, auth_uc: IAuthenticateUserUseCase):
        self.auth_uc = auth_uc

    def get(self):
        if current_user.is_authenticated:
            return redirect(url_for("main.index"))
        form = LoginForm()
        return render_template("login.html", form=form)

    def post(self):
        if current_user.is_authenticated:
            return redirect(url_for("main.index"))
        form = LoginForm()
        if form.validate_on_submit():  # type: ignore
            try:
                user_dto = self.auth_uc.execute(
                    username=str(form.username.data),
                    password=str(form.password.data),
                )

                role = self.get_role(user_dto)
                user = FlaskUserDescriptor(
                    user_id=user_dto.id, username=user_dto.username, role=role
                )

                login_user(user, remember=form.remember_me.data)
                flash("Logged in.", "success")
                return redirect(url_for("main.index"))

            except InvalidCredentialsError:
                flash("Invalid credentials.", "error")
            except NotFoundError:
                flash(
                    f"User with username {form.username.data} does not exist.",
                    "error",
                )
            except Exception as e:
                flash(str(e), "error")

        return render_template("login.html", form=form)

    def get_role(self, user: UserDTO) -> Role:
        match user.role:
            case self.admin_role.name:
                return self.admin_role
            case self.user_role.name:
                return self.user_role
            case _:
                raise ValueError("Unknown role")


class LogoutView(MethodView):
    def __init__(self, logout_uc: ILogoutUserUseCase):
        self.logout_uc = logout_uc

    @login_required
    def get(self):
        try:
            desc = get_current_user()
            self.logout_uc.execute(descriptor=desc)
            logout_user()
            flash("Logged out.", "success")
        except Exception as e:
            flash(str(e), "error")
        return redirect(url_for("main.index"))

    def post(self):
        return self.get()
