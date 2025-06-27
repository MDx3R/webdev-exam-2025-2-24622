from http import HTTPStatus
from typing import Any

import pytest
from flask import Flask
from sqlalchemy.orm import Session

from di.container import Container
from infrastructure.sqlalchemy.models.recipe.recipe import RecipeModel
from infrastructure.sqlalchemy.models.review import ReviewModel
from presentation.web.flask.main import FlaskUserDescriptor


class TestRecipeViews:
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
            title="Test Recipe",
            description="A test recipe description",
            preparation_time=60,
            servings=4,
            ingredients="Ingredient 1, Ingredient 2",
            steps="Step 1. Do this. Step 2. Do that.",
            author_id=self.user.user_id,
        )
        yield

    def add_recipe(self, recipe: RecipeModel):
        session: Session = self.container.database().get_session_factory()()
        session.add(recipe)
        session.commit()

    def test_recipe_view_get_success(self):
        self.add_recipe(self.recipe)
        response = self.client.get(f"/recipes/{self.recipe.id}")

        assert response.status_code == HTTPStatus.OK
        assert self.recipe.title in response.text  # type: ignore
        assert self.recipe.description in response.text  # type: ignore

    def test_recipe_view_get_not_found(self):
        response = self.client.get("/recipes/999", follow_redirects=True)

        assert "Recipe not found." in response.text

    def test_recipe_add_get_when_authenticated(self):
        client = self.app.test_client(user=self.user)
        response = client.get("/recipes/add")

        assert response.status_code == HTTPStatus.OK
        assert "Добавить" in response.text

    def test_recipe_add_get_redirects_when_unauthenticated(self):
        response = self.client.get("/recipes/add")

        loc = response.headers.get("Location")
        assert loc
        assert "/auth/login" in loc

    def test_recipe_add_post_success_when_authenticated(self):
        client = self.app.test_client(user=self.user)
        form_data = {
            "title": "New Recipe",
            "description": "A new recipe",
            "preparation_time": "45",
            "servings": "2",
            "ingredients": "Flour, Sugar",
            "steps": "Mix and bake.",
        }
        response = client.post(
            "/recipes/add", data=form_data, follow_redirects=True
        )

        assert response.status_code == HTTPStatus.OK
        assert b"Recipe created successfully." in response.data

        session: Session = self.container.database().get_session_factory()()
        recipe = (
            session.query(RecipeModel).filter_by(title="New Recipe").first()
        )
        assert recipe is not None
        assert recipe.author_id == self.user.user_id  # type: ignore

    def test_recipe_add_post_redirects_when_unauthenticated(self):
        form_data = {
            "title": "New Recipe",
            "description": "A new recipe",
            "preparation_time": "45",
            "servings": "2",
            "ingredients": "Flour, Sugar",
            "steps": "Mix and bake.",
        }
        response = self.client.post("/recipes/add", data=form_data)

        loc = response.headers.get("Location")
        assert loc
        assert "/auth/login" in loc

    def test_recipe_add_post_invalid_form(self):
        client = self.app.test_client(user=self.user)
        form_data = {
            "title": "",  # Пустой заголовок
            "description": "A new recipe",
            "preparation_time": "45",
            "servings": "2",
            "ingredients": "Flour, Sugar",
            "steps": "Mix and bake.",
        }
        response = client.post("/recipes/add", data=form_data)

        assert response.status_code == HTTPStatus.OK
        assert "Добавить" in response.text  # Страница не иземенилась

    def test_recipe_edit_get_author(self):
        self.add_recipe(self.recipe)
        client = self.app.test_client(user=self.user)
        response = client.get(f"/recipes/{self.recipe.id}/edit")

        assert response.status_code == HTTPStatus.OK
        assert self.recipe.title in response.text  # type: ignore

    def test_recipe_edit_get_admin(self):
        self.add_recipe(self.recipe)
        client = self.app.test_client(user=self.admin)
        response = client.get(f"/recipes/{self.recipe.id}/edit")

        assert response.status_code == HTTPStatus.OK
        assert self.recipe.title in response.text  # type: ignore

    def test_recipe_edit_get_unauthorized(
        self, third_user_descriptor: FlaskUserDescriptor
    ):
        self.add_recipe(self.recipe)
        client = self.app.test_client(user=third_user_descriptor)
        response = client.get(
            f"/recipes/{self.recipe.id}/edit", follow_redirects=True
        )

        assert response.status_code == HTTPStatus.OK
        assert "No permission." in response.text

    def test_recipe_edit_post_success(self):
        self.add_recipe(self.recipe)
        client = self.app.test_client(user=self.user)
        form_data: dict[str, Any] = {
            "title": "Updated Recipe",
            "description": self.recipe.description,
            "preparation_time": str(self.recipe.preparation_time),
            "servings": str(self.recipe.servings),
            "ingredients": self.recipe.ingredients,
            "steps": self.recipe.steps,
        }
        response = client.post(
            f"/recipes/{self.recipe.id}/edit",
            data=form_data,
            follow_redirects=True,
        )

        assert response.status_code == HTTPStatus.OK
        assert b"Recipe updated." in response.data

        session: Session = self.container.database().get_session_factory()()
        recipe = (
            session.query(RecipeModel).filter_by(id=self.recipe.id).first()
        )
        assert recipe.title == "Updated Recipe"  # type: ignore

    def test_recipe_edit_post_unauthorized(
        self, third_user_descriptor: FlaskUserDescriptor
    ):
        self.add_recipe(self.recipe)
        client = self.app.test_client(user=third_user_descriptor)
        form_data: dict[str, Any] = {
            "title": "Updated Recipe",
            "description": self.recipe.description,
            "preparation_time": str(self.recipe.preparation_time),
            "servings": str(self.recipe.servings),
            "ingredients": self.recipe.ingredients,
            "steps": self.recipe.steps,
        }
        response = client.post(
            f"/recipes/{self.recipe.id}/edit",
            data=form_data,
            follow_redirects=True,
        )

        assert response.status_code == HTTPStatus.OK
        assert (
            "Insufficient permissions to change this recipe." in response.text
        )

    def test_recipe_delete_post_authorized(self):
        self.add_recipe(self.recipe)
        client = self.app.test_client(user=self.user)
        response = client.post(
            f"/recipes/{self.recipe.id}/delete", follow_redirects=True
        )

        assert response.status_code == HTTPStatus.OK
        assert b"Recipe deleted." in response.data

        session: Session = self.container.database().get_session_factory()()
        recipe = (
            session.query(RecipeModel).filter_by(id=self.recipe.id).first()
        )
        assert recipe is None

    def test_recipe_delete_post_unauthorized(
        self, third_user_descriptor: FlaskUserDescriptor
    ):
        self.add_recipe(self.recipe)
        client = self.app.test_client(user=third_user_descriptor)
        response = client.post(
            f"/recipes/{self.recipe.id}/delete", follow_redirects=True
        )

        assert response.status_code == HTTPStatus.OK
        assert (
            "Insufficient permissions to change this recipe." in response.text
        )

    def test_review_create_post_success(self):
        self.add_recipe(self.recipe)
        client = self.app.test_client(user=self.user)
        form_data = {
            "rating": "5",
            "text": "Great recipe!",
        }
        response = client.post(
            f"/recipes/{self.recipe.id}/review",
            data=form_data,
            follow_redirects=True,
        )

        assert response.status_code == HTTPStatus.OK
        assert b"Review added." in response.data

        session: Session = self.container.database().get_session_factory()()
        review = (
            session.query(ReviewModel)
            .filter_by(recipe_id=self.recipe.id)
            .first()
        )
        assert review is not None
        assert review.rating == 5  # type: ignore
        assert review.text == "Great recipe!"  # type: ignore
        assert review.user_id == self.user.user_id  # type: ignore

    def test_review_create_post_invalid_form(self):
        self.add_recipe(self.recipe)
        client = self.app.test_client(user=self.user)
        form_data = {
            "rating": "",  # Нет рейтинга
            "text": "Great recipe!",
        }
        response = client.post(
            f"/recipes/{self.recipe.id}/review",
            data=form_data,
            follow_redirects=True,
        )

        assert response.status_code == HTTPStatus.OK
        assert b"Review added." not in response.data
