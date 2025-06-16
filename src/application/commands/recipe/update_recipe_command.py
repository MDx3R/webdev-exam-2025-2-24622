from dataclasses import dataclass


@dataclass(frozen=True)
class UpdateRecipeCommand:
    recipe_id: int
    title: str
    description: str
    preparation_time: int
    servings: int
    ingredients: str
    steps: str
