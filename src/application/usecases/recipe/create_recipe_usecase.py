from uuid import uuid4

from application.commands.recipe.create_recipe_command import (
    CreateRecipeCommand,
)
from application.dtos.recipe.recipe_dto import RecipeDTO
from application.dtos.user.user_descriptor import UserDescriptor
from application.interfaces.services.image_store import IImageStore
from application.interfaces.usecases.recipe.create_recipe_usecase import (
    ICreateRecipeUseCase,
)
from application.transactions.transactional import transactional
from domain.entities.recipe.dtos import RecipeData, RecipeImageData
from domain.entities.recipe.factories import (
    IRecipeFactory,
    IRecipeImageFactory,
)
from domain.repositories.recipe_repository import IRecipeRepository


class CreateRecipeUseCase(ICreateRecipeUseCase):
    def __init__(
        self,
        recipe_factory: IRecipeFactory,
        image_factory: IRecipeImageFactory,
        recipe_repository: IRecipeRepository,
        image_store: IImageStore,
    ):
        self.recipe_factory = recipe_factory
        self.image_factory = image_factory
        self.recipe_repository = recipe_repository
        self.image_store = image_store

    @transactional
    def execute(
        self, command: CreateRecipeCommand, descriptor: UserDescriptor
    ) -> RecipeDTO:
        recipe = self.recipe_factory.create(
            RecipeData(
                title=command.title,
                description=command.description,
                preparation_time=command.preparation_time,
                servings=command.servings,
                ingredients=command.ingredients,
                steps=command.steps,
                author_id=descriptor.user_id,
            )
        )

        recipe = self.recipe_repository.save(recipe)

        if command.images:
            images = [
                (
                    self.image_factory.create(
                        RecipeImageData(
                            filename=str(uuid4()),
                            mime_type=i.mime_type,
                            recipe_id=recipe.id_safe.value,
                        )
                    ),
                    i.content,
                )
                for i in command.images
            ]

            for image, content in images:
                recipe.add_image(image)
                self.image_store.upload(image.filename, content)

            recipe = self.recipe_repository.save(recipe)

        # TODO: Сохранять фото
        return RecipeDTO.from_domain(recipe)
