from dataclasses import dataclass

from domain.entities.recipe.image import RecipeImage


@dataclass
class ImageDTO:
    filename: str
    mime_type: str

    @classmethod
    def from_domain(cls, image: RecipeImage) -> "ImageDTO":
        return cls(filename=image.filename, mime_type=image.mime_type)
