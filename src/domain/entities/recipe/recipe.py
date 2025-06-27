from dataclasses import dataclass, field

from domain.entities.entity import Entity, Id
from domain.entities.recipe.value_objects import (
    RecipeContent,
    RecipeDetails,
    RecipeInstruction,
)
from domain.entities.user.role import Role, RoleEnum

from .image import RecipeImage


@dataclass
class Recipe(Entity):
    """
    Aggregate root for Recipe.
    """

    content: RecipeContent
    details: RecipeDetails
    instruction: RecipeInstruction
    author_id: Id
    images: list[RecipeImage] = field(default_factory=list[RecipeImage])

    def __post_init__(self):
        assert self.author_id, "Author ID is required."

    @property
    def recipe_id(self) -> Id | None:
        return self.id

    def is_owner(self, user_id: int) -> bool:
        return self.author_id.value == user_id

    def can_mutate(self, user_id: int, role: Role) -> bool:
        return role == RoleEnum.ADMIN.value or self.is_owner(user_id)

    def ensure_can_mutate(self, user_id: int, role: Role):
        if not self.can_mutate(user_id, role):
            raise PermissionError(
                "Insufficient permissions to change this recipe."
            )

    def update(
        self,
        content: RecipeContent,
        details: RecipeDetails,
        instruction: RecipeInstruction,
    ):
        self.content = content
        self.details = details
        self.instruction = instruction

    def add_image(self, image: RecipeImage) -> None:
        self.images.append(image)

    def remove_image(self, image_id: int) -> None:
        self.images = [
            img
            for img in self.images
            if (img.image_id.value != image_id if img.image_id else True)
        ]

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
            entity_id=None,
            content=content,
            details=details,
            instruction=instruction,
            author_id=Id(author_id),
            images=images,
        )
