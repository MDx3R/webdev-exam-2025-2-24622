from dataclasses import dataclass, field

from .image import RecipeImage


@dataclass
class Recipe:
    """
    Aggregate root for Recipe.
    """

    recipe_id: int
    title: str
    description: str
    preparation_time: int
    servings: int
    ingredients: str
    steps: str
    author_id: int
    images: list[RecipeImage] = field(default_factory=list[RecipeImage])

    def __post_init__(self):
        assert self.title, "Title is required."
        assert self.description, "Description is required."
        assert self.preparation_time > 0, "Preparation time must be positive."
        assert self.servings > 0, "Servings must be positive."
        assert self.ingredients, "Ingredients are required."
        assert self.steps, "Steps are required."

    def add_image(self, image: RecipeImage) -> None:
        self.images.append(image)

    def remove_image(self, image_id: int) -> None:
        self.images = [img for img in self.images if img.image_id != image_id]
