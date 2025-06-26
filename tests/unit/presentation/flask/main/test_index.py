from http import HTTPStatus
from unittest.mock import Mock

import pytest
from dependency_injector import providers
from flask import Flask
from tests.unit.presentation.flask.conftest import Container

from application.dtos.recipe.recipe_dto import RecipeSummaryDTO
from application.interfaces.usecases.recipe.list_recipes_usecase import (
    IListRecipesUseCase,
)
from domain.entities.user.role import RoleEnum
from presentation.web.flask.main import FlaskUserDescriptor


class TestIndex:
    @pytest.fixture(autouse=True)
    def setup(self, app: Flask, container: Container):
        self.app = app
        self.container = container
        self.client = app.test_client()
        self.recipe = RecipeSummaryDTO(1, "title", 60, 4, 4.56767, 5, 2, [])
        self.recipes = [self.recipe]
        yield

    def mock_list_recipes_uc(self, recipes: list[RecipeSummaryDTO]):
        mock = Mock(spec=IListRecipesUseCase)
        mock.execute.return_value = recipes

        self.container.override_providers(
            list_recipes_uc=providers.Object(mock)
        )

    def test_index(self):
        self.mock_list_recipes_uc(self.recipes)

        response = self.client.get("/")

        assert "title" in response.text
        assert "60" in response.text
        assert "4" in response.text
        assert "4.57" in response.text  # rounding
        assert "5" in response.text
        assert "1" in response.text

    def test_index_processes_empty_list(self):
        self.mock_list_recipes_uc([])

        response = self.client.get("/")

        assert response.status_code == HTTPStatus.OK

    def test_index_has_buttons_for_author(self):
        user = FlaskUserDescriptor(
            self.recipe.author_id, "username", RoleEnum.USER.value
        )
        client = self.app.test_client(user=user)
        self.mock_list_recipes_uc(self.recipes)

        response = client.get("/")

        assert "Редактировать" in response.text
        assert "Удалить" in response.text

    def test_index_has_buttons_for_admin(self):
        user = FlaskUserDescriptor(1, "username", RoleEnum.ADMIN.value)
        client = self.app.test_client(user=user)
        self.mock_list_recipes_uc(self.recipes)

        response = client.get("/")

        assert "Редактировать" in response.text
        assert "Удалить" in response.text
