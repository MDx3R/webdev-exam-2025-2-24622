from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    url_for,
)
from flask_login import (  # type: ignore
    current_user,
    login_required,  # type: ignore
    login_user,  # type: ignore
    logout_user,
)

from application.exceptions import InvalidCredentialsError
from domain.entities.user.role import RoleEnum
from presentation.web.flask.forms import LoginForm
from presentation.web.flask.main import FlaskUserDescriptor
from presentation.web.flask.utils import get_container


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    admin = RoleEnum.ADMIN.value
    user = RoleEnum.USER.value
    use_case = get_container().auth_uc()

    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = LoginForm()
    if form.validate_on_submit():  # type: ignore
        try:
            user_dto = use_case.execute(
                username=form.username.data, password=form.password.data  # type: ignore
            )
            match user_dto.id:
                case admin.id_safe.value:
                    role = admin
                case user.id_safe.value:
                    role = user
                case _:
                    raise ValueError("Unknown role")

            user = FlaskUserDescriptor(
                user_id=user_dto.id, username=user_dto.username, role=role
            )

            login_user(user, remember=form.remember_me.data)

            flash("Logged in.", "success")
            return redirect(url_for("main.index"))
        except InvalidCredentialsError:
            flash("Invalid credentials.", "error")
        except Exception as e:
            flash(str(e), "error")
    return render_template("login.html", form=form)


@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    use_case = get_container().logout_uc()

    try:
        use_case.execute(descriptor=current_user)  # type: ignore
        logout_user()
        flash("Logged out.", "success")
    except Exception as e:
        flash(str(e), "error")

    return redirect(url_for("main.index"))
