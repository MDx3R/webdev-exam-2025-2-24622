from dataclasses import dataclass
from typing import Self

from domain.entities.recipe.image import RecipeImage


@dataclass
class ImageDTO:
    filename: str
    mime_type: str

    @classmethod
    def from_domain(cls, image: RecipeImage) -> Self:
        return cls(filename=image.filename, mime_type=image.mime_type)
