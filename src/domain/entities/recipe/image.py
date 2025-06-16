from dataclasses import dataclass


@dataclass
class RecipeImage:
    """
    Entity representing an image associated with a recipe.
    """

    image_id: int | None
    filename: str
    mime_type: str
    recipe_id: int

    def __post_init__(self):
        assert self.filename, "Filename is required."
        assert self.mime_type, "MIME type is required."

    @classmethod
    def create(
        cls, filename: str, mime_type: str, recipe_id: int
    ) -> "RecipeImage":
        return cls(
            image_id=None,
            filename=filename,
            mime_type=mime_type,
            recipe_id=recipe_id,
        )
