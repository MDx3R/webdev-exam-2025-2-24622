import pytest

from application.exceptions import NotFoundError
from domain.entities.entity import Id
from domain.entities.recipe.image import RecipeImage
from domain.entities.recipe.recipe import Recipe
from domain.entities.recipe.value_objects import (
    RecipeContent,
    RecipeDetails,
    RecipeInstruction,
)
from domain.entities.user.role import RoleEnum
from domain.entities.user.user import User
from domain.entities.user.value_objects import FullName
from infrastrcuture.sqlalchemy.repositories.recipe_repository import (
    SQLAlchemyRecipeRepository,
)
from infrastrcuture.sqlalchemy.repositories.user_repository import (
    SQLAlchemyUserRepository,
)
from infrastrcuture.sqlalchemy.transactions import SQLAlchemyTransactionManager


class Counter:
    counter = 0


class TestSQLAlchemyRecipeRepository:
    @pytest.fixture(autouse=True)
    def setup(
        self,
        recipe_repository: SQLAlchemyRecipeRepository,
        user_repository: SQLAlchemyUserRepository,
        transaction_manager: SQLAlchemyTransactionManager,
    ):
        self.recipe_repository = recipe_repository
        self.user_repository = user_repository
        self.transaction_manager = transaction_manager

    def _get_user(self) -> User:
        Counter.counter += 1
        return User(
            entity_id=Id(Counter.counter),
            username=f"username{Counter.counter}",
            full_name=FullName(surname="Doe", name="John", patronymic=None),
            password_hash="hash",
            role=RoleEnum.USER.value,
        )

    def _get_recipe(self, author_id: int) -> Recipe:
        Counter.counter += 1
        return Recipe(
            entity_id=Id(Counter.counter),
            content=RecipeContent(
                title=f"Recipe {Counter.counter}", description="Delicious dish"
            ),
            details=RecipeDetails(preparation_time=30, servings=4),
            instruction=RecipeInstruction(
                ingredients="Flour, Sugar", steps="Mix and bake"
            ),
            author_id=Id(author_id),
            images=[
                RecipeImage(
                    entity_id=Id(Counter.counter + 1),
                    filename="image.jpg",
                    mime_type="image/jpeg",
                    recipe_id=Id(Counter.counter),
                )
            ],
        )

    def test_get_by_id_success(self):
        user = self._get_user()
        with self.transaction_manager:
            saved_user = self.user_repository.save(user)
            recipe = self._get_recipe(saved_user.id_safe.value)
            saved_recipe = self.recipe_repository.save(recipe)

        with self.transaction_manager:
            retrieved_recipe = self.recipe_repository.get_by_id(
                saved_recipe.id_safe.value
            )

        assert retrieved_recipe is not None
        assert retrieved_recipe.content.title == recipe.content.title
        assert len(retrieved_recipe.images) == len(recipe.images)
        assert retrieved_recipe.author_id == saved_user.id

    def test_get_by_id_not_found(self):
        with self.transaction_manager:
            with pytest.raises(NotFoundError, match="Recipe"):
                self.recipe_repository.get_by_id(999)

    def test_get_all_success(self):
        user = self._get_user()
        with self.transaction_manager:
            saved_user = self.user_repository.save(user)
            recipe1 = self._get_recipe(saved_user.id_safe.value)
            recipe2 = self._get_recipe(saved_user.id_safe.value)
            self.recipe_repository.save(recipe1)
            self.recipe_repository.save(recipe2)

        with self.transaction_manager:
            recipes = self.recipe_repository.get_all(page=1, per_page=10)

        assert len(recipes) == 2
        assert all(isinstance(r, Recipe) for r in recipes)

    def test_get_all_empty(self):
        with self.transaction_manager:
            recipes = self.recipe_repository.get_all(page=1, per_page=10)

        assert isinstance(recipes, list)

    def test_save_recipe_success(self):
        user = self._get_user()
        with self.transaction_manager:
            saved_user = self.user_repository.save(user)
            recipe = self._get_recipe(saved_user.id_safe.value)
            saved_recipe = self.recipe_repository.save(recipe)

        with self.transaction_manager:
            retrieved_recipe = self.recipe_repository.get_by_id(
                saved_recipe.id_safe.value
            )
            assert retrieved_recipe.content.title == recipe.content.title
            assert (
                retrieved_recipe.details.preparation_time
                == recipe.details.preparation_time
            )
            assert len(retrieved_recipe.images) == len(recipe.images)

    def test_remove_recipe_success(self):
        user = self._get_user()
        with self.transaction_manager:
            saved_user = self.user_repository.save(user)
            recipe = self._get_recipe(saved_user.id_safe.value)
            saved_recipe = self.recipe_repository.save(recipe)

        with self.transaction_manager:
            self.recipe_repository.remove(saved_recipe)

        with self.transaction_manager:
            with pytest.raises(NotFoundError, match="Recipe"):
                self.recipe_repository.get_by_id(saved_recipe.id_safe.value)
