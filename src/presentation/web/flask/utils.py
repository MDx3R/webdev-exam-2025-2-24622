from flask import current_app
from flask_login import current_user  # type: ignore

from di.container import Container
from presentation.web.flask.main import FlaskUserDescriptor


def get_container() -> Container:
    return current_app.extensions["di_container"]


def get_current_user() -> FlaskUserDescriptor:
    return current_user  # type: ignore
