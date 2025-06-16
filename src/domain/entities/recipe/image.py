from dataclasses import dataclass

from domain.constants import ALLOWED_MIME_TYPES
from domain.entities.entity import Entity, Id


@dataclass
class RecipeImage(Entity):
    """
    Entity representing an image associated with a recipe.
    """

    filename: str
    mime_type: str
    recipe_id: Id

    def __post_init__(self):
        assert self.filename.strip(), "Filename is required."
        assert self.mime_type.strip(), "MIME type is required."
        assert (
            self.mime_type in ALLOWED_MIME_TYPES
        ), f"Invalid MIME type. Valid values: {ALLOWED_MIME_TYPES}"
        assert self.recipe_id, "Recipe ID is required."

    @property
    def image_id(self) -> Id | None:
        return self.id

    @classmethod
    def create(
        cls, filename: str, mime_type: str, recipe_id: int
    ) -> "RecipeImage":
        return cls(
            entity_id=None,
            filename=filename.strip(),
            mime_type=mime_type.strip(),
            recipe_id=Id(recipe_id),
        )
