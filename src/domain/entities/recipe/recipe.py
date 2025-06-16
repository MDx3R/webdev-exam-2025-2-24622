from dataclasses import dataclass, field

from domain.entities.recipe.value_objects import (
    RecipeContent,
    RecipeDetails,
    RecipeInstruction,
)

from .image import RecipeImage


@dataclass
class Recipe:
    """
    Aggregate root for Recipe.
    """

    recipe_id: int | None
    content: RecipeContent
    details: RecipeDetails
    instruction: RecipeInstruction
    author_id: int
    images: list[RecipeImage] = field(default_factory=list[RecipeImage])

    def add_image(self, image: RecipeImage) -> None:
        self.images.append(image)

    def remove_image(self, image_id: int) -> None:
        self.images = [img for img in self.images if img.image_id != image_id]

    @classmethod
    def create(
        cls,
        content: RecipeContent,
        details: RecipeDetails,
        instruction: RecipeInstruction,
        author_id: int,
        images: list[RecipeImage],
    ) -> "Recipe":
        return cls(
            recipe_id=None,
            content=content,
            details=details,
            instruction=instruction,
            author_id=author_id,
            images=images,
        )
