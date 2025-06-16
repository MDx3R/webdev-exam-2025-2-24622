from dataclasses import dataclass


@dataclass
class RecipeImage:
    """
    Entity representing an image associated with a recipe.
    """

    image_id: int
    filename: str
    mime_type: str
    recipe_id: int

    def __post_init__(self):
        assert self.filename, "Filename is required."
        assert self.mime_type, "MIME type is required."
