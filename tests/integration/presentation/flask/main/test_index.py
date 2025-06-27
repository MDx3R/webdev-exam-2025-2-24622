from http import HTTPStatus

import pytest
from flask import Flask

from di.container import Container
from infrastructure.sqlalchemy.models.recipe.recipe import RecipeModel
from presentation.web.flask.main import FlaskUserDescriptor


class TestIndex:
    @pytest.fixture(autouse=True)
    def setup(
        self,
        flask_app: Flask,
        container: Container,
        admin_descriptor: FlaskUserDescriptor,
        user_descriptor: FlaskUserDescriptor,
    ):
        self.app = flask_app
        self.container = container
        self.admin = admin_descriptor
        self.user = user_descriptor
        self.client = flask_app.test_client()
        self.recipe = RecipeModel(
            id=1,
            title="title",
            description="description",
            preparation_time=60,
            servings=4,
            ingredients="ingredients",
            steps="steps",
            author_id=self.user.user_id,
        )
        yield

    def add_recipe(self, recipe: RecipeModel):
        session = self.container.database().get_session_factory()()
        session.add(recipe)
        session.commit()

    def test_index_processes_empty_list(self):
        response = self.client.get("/")

        assert response.status_code == HTTPStatus.OK

    def test_index(self):
        self.add_recipe(self.recipe)

        response = self.client.get("/")

        assert self.recipe.title in response.text  # type: ignore

    def test_index_has_buttons_for_author(self):
        self.add_recipe(self.recipe)
        client = self.app.test_client(user=self.user)

        response = client.get("/")

        assert "Редактировать" in response.text
        assert "Удалить" in response.text

    def test_index_has_buttons_for_admin(self):
        self.add_recipe(self.recipe)
        client = self.app.test_client(user=self.admin)

        response = client.get("/")

        assert "Редактировать" in response.text
        assert "Удалить" in response.text
