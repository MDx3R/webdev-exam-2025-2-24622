from flask import Blueprint, Flask
from flask_cors import CORS

from di.container import Container
from presentation.web.flask.main import init_login_manager


class FlaskServer:
    def __init__(self, container: Container):
        self.app = Flask(
            __name__,
            static_folder="../../presentation/web/flask/static",
            template_folder="../../presentation/web/flask/templates",
        )
        self.container = container
        CORS(self.app, supports_credentials=True)

    def configure(self):
        init_login_manager(self.app, self.container.user_repo())

    def setup_routes(self):
        self._register_auth_routers()

    def _register_main_routers(self):
        from presentation.web.flask.blueprints.main import main_bp

        self._include_blueprint(main_bp, "/")

    def _register_auth_routers(self):
        from presentation.web.flask.blueprints.auth import auth_bp

        self._include_blueprint(auth_bp, "/auth")

    def _register_recipe_routers(self):
        from presentation.web.flask.blueprints.recipes import recipes_bp

        self._include_blueprint(recipes_bp, "/recipe")

    def _include_blueprint(self, blueprint: Blueprint, prefix: str):
        self.app.register_blueprint(blueprint, url_prefix=prefix)
