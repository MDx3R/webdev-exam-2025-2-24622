from typing import cast

from sqlalchemy import delete, select
from sqlalchemy.orm import selectinload

from application.exceptions import ApplicationError, NotFoundError
from domain.entities.entity import Id
from domain.entities.recipe.image import RecipeImage
from domain.entities.recipe.recipe import Recipe
from domain.entities.recipe.value_objects import (
    RecipeContent,
    RecipeDetails,
    RecipeInstruction,
)
from domain.repositories.recipe_repository import IRecipeRepository
from infrastructure.sqlalchemy.models import RecipeImageModel, RecipeModel
from infrastructure.sqlalchemy.query_executor import QueryExecutor
from infrastructure.sqlalchemy.transactions import SQLAlchemyTransactionManager


class SQLAlchemyRecipeRepository(IRecipeRepository):
    def __init__(
        self,
        query_executor: QueryExecutor,
        transaction_manager: SQLAlchemyTransactionManager,
    ):
        self.query_executor = query_executor
        self.transaction_manager = transaction_manager

    def get_by_id(self, recipe_id: int) -> Recipe:
        statement = (
            select(RecipeModel)
            .options(selectinload(RecipeModel.images))
            .where(RecipeModel.id == recipe_id)
        )
        recipe_model = self.query_executor.execute_scalar_one(statement)
        if not recipe_model:
            raise NotFoundError(recipe_id, "Recipe")
        return self._to_domain(recipe_model)

    def get_all(self, page: int, per_page: int) -> list[Recipe]:
        offset = (page - 1) * per_page
        statement = (
            select(RecipeModel)
            .options(selectinload(RecipeModel.images))
            .order_by(RecipeModel.system_created_at.desc())
            .offset(offset)
            .limit(per_page)
        )
        recipe_models = self.query_executor.execute_scalar_many(statement)
        return [self._to_domain(model) for model in recipe_models]

    def save(self, recipe: Recipe) -> Recipe:
        with self.transaction_manager.get_session():
            recipe_model = self._to_model(recipe)
            self.query_executor.save(recipe_model)
            # Add images
            image_models = [
                RecipeImageModel(
                    filename=img.filename,
                    mime_type=img.mime_type,
                    recipe_id=recipe_model.id,
                )
                for img in recipe.images
            ]
            if image_models:
                self.query_executor.add_all(image_models)
            return self._to_domain(recipe_model)

    def remove(self, recipe: Recipe) -> None:
        if not recipe.id:
            raise ApplicationError("Recipe without id cannot be removed")
        statement = delete(RecipeModel).where(
            RecipeModel.id == recipe.id_safe.value
        )
        self.query_executor.execute(statement)

    def _to_domain(self, model: RecipeModel) -> Recipe:
        recipe = Recipe(
            entity_id=Id(cast(int, model.id)),
            content=RecipeContent(
                cast(str, model.title),
                cast(str, model.description),
            ),
            details=RecipeDetails(
                cast(int, model.preparation_time),
                cast(int, model.servings),
            ),
            instruction=RecipeInstruction(
                cast(str, model.ingredients),
                cast(str, model.steps),
            ),
            author_id=Id(cast(int, model.author_id)),
            images=[
                RecipeImage(
                    entity_id=Id(img.id),
                    filename=img.filename,
                    mime_type=img.mime_type,
                    recipe_id=Id(img.recipe_id),
                )
                for img in model.images
            ],
        )
        return recipe

    def _to_model(self, recipe: Recipe) -> RecipeModel:
        return RecipeModel(
            id=recipe.id.value if recipe.id else None,
            title=recipe.content.title,
            description=recipe.content.description,
            preparation_time=recipe.details.preparation_time,
            servings=recipe.details.servings,
            ingredients=recipe.instruction.ingredients,
            steps=recipe.instruction.steps,
            author_id=recipe.author_id.value,
        )
