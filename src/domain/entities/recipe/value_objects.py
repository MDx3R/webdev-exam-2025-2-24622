from dataclasses import dataclass


@dataclass(frozen=True)
class RecipeContent:
    title: str
    description: str

    def __post_init__(self):
        assert self.title.strip(), "Title is required."
        assert self.description.strip(), "Description is required."

    @classmethod
    def create(cls, title: str, description: str) -> "RecipeContent":
        return cls(title=title.strip(), description=description.strip())


@dataclass(frozen=True)
class RecipeInstruction:
    ingredients: str
    steps: str

    def __post_init__(self):
        assert self.ingredients.strip(), "Ingredients are required."
        assert self.steps.strip(), "Steps are required."

    @classmethod
    def create(cls, ingredients: str, steps: str) -> "RecipeInstruction":
        return cls(ingredients=ingredients.strip(), steps=steps.strip())


@dataclass(frozen=True)
class RecipeDetails:
    preparation_time: int
    servings: int

    def __post_init__(self):
        assert self.preparation_time > 0, "Preparation time must be positive."
        assert self.servings > 0, "Servings must be positive."

    @classmethod
    def create(cls, preparation_time: int, servings: int) -> "RecipeDetails":
        return cls(preparation_time=preparation_time, servings=servings)
