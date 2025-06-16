from dataclasses import dataclass

from application.commands.recipe.upload_image_command import UploadImageCommand


@dataclass(frozen=True)
class CreateRecipeCommand:
    title: str
    description: str
    preparation_time: int
    servings: int
    ingredients: str
    steps: str
    images: list[UploadImageCommand]
