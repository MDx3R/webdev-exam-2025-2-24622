from dataclasses import dataclass


@dataclass(frozen=True)
class RecipeImageData:
    filename: str
    mime_type: str
    recipe_id: int


@dataclass(frozen=True)
class RecipeData:
    title: str
    description: str
    preparation_time: int
    servings: int
    ingredients: str
    steps: str
    author_id: int
    images: list[RecipeImageData]
