import os

from flask import Flask
from flask.typing import RouteCallable
from flask_cors import CORS

from di.container import Container
from infrastructure.config.config import AuthConfig


class FlaskServer:
    def __init__(self, base_dir: str, container: Container, auth: AuthConfig):
        self.app = Flask(
            __name__,
            static_folder=os.path.join(base_dir, "static"),
            template_folder=os.path.join(base_dir, "templates"),
        )
        self.container = container
        self.app.extensions["di_container"] = container
        self.app.secret_key = auth.SECRET_KEY
        self.login_manager = container.login_manager()

        CORS(self.app, supports_credentials=True)

    def configure(self):
        self.login_manager.configure(self.app)
        self.login_manager.set_login_view("auth.login")
        self.login_manager.set_login_message(
            "Для доступа к данной странице необходимо пройти процедуру аутентификации."
        )
        self.login_manager.set_login_message_category("warning")

    def setup_routes(self):
        self._register_auth_views()
        self._register_main_views()
        self._register_recipe_views()

        print("Registered routes:")
        for rule in self.app.url_map.iter_rules():
            print(rule)
        print("Done")

    def _register_auth_views(self):
        from presentation.web.flask.blueprints.auth import (
            LoginView,
            LogoutView,
        )

        self._add_view(
            "/auth/login",
            LoginView.as_view("auth.login", auth_uc=self.container.auth_uc()),
        )
        self._add_view(
            "/auth/logout",
            LogoutView.as_view(
                "auth.logout", logout_uc=self.container.logout_uc()
            ),
        )

    def _register_main_views(self):
        from presentation.web.flask.blueprints.main import IndexView

        self._add_view(
            "/",
            IndexView.as_view(
                "main.index", list_recipes_uc=self.container.list_recipes_uc()
            ),
        )

    def _register_recipe_views(self):
        from presentation.web.flask.blueprints.recipes import (
            RecipeAddView,
            RecipeDeleteView,
            RecipeEditView,
            RecipeView,
            ReviewCreateView,
        )

        self._add_view(
            "/recipes/<int:recipe_id>",
            RecipeView.as_view(
                "recipes.recipe_view",
                get_recipe_uc=self.container.get_recipe_uc(),
                markdown_renderer=self.container.markdown_renderer(),
            ),
        )
        self._add_view(
            "/recipes/add",
            RecipeAddView.as_view(
                "recipes.recipe_add",
                create_recipe_uc=self.container.create_recipe_uc(),
            ),
        )
        self._add_view(
            "/recipes/<int:recipe_id>/edit",
            RecipeEditView.as_view(
                "recipes.recipe_edit",
                update_recipe_uc=self.container.update_recipe_uc(),
                get_recipe_uc=self.container.get_recipe_uc(),
            ),
        )
        self._add_view(
            "/recipes/<int:recipe_id>/delete",
            RecipeDeleteView.as_view(
                "recipes.recipe_delete",
                delete_recipe_uc=self.container.delete_recipe_uc(),
            ),
        )
        self._add_view(
            "/recipes/<int:recipe_id>/review",
            ReviewCreateView.as_view(
                "recipes.review_create",
                create_review_uc=self.container.create_review_uc(),
            ),
        )

    def _add_view(
        self,
        route: str,
        view_func: RouteCallable,
    ):
        self.app.add_url_rule(route, view_func=view_func)
