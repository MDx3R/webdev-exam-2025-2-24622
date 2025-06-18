from flask import current_app

from di.container import Container


def get_container() -> Container:
    return current_app.extensions["di_container"]
