from abc import ABC, abstractmethod
from dataclasses import replace

from application.dtos.recipe.recipe_dto import FullRecipeDTO, RecipeDTO
from application.dtos.review.review_dto import AuthoredReviewDTO, ReviewDTO


class IMarkdownRenderer(ABC):
    @abstractmethod
    def render(self, text: str) -> str: ...

    def render_recipe(self, recipe: RecipeDTO) -> RecipeDTO:
        description = self.render(recipe.description)
        ingredients = self.render(recipe.ingredients)
        steps = self.render(recipe.steps)
        return replace(
            recipe,
            description=description,
            ingredients=ingredients,
            steps=steps,
        )

    def render_review(self, review: ReviewDTO) -> ReviewDTO:
        text = self.render(review.text)
        return replace(review, text=text)

    def render_authored_review(
        self, authored_review: AuthoredReviewDTO
    ) -> AuthoredReviewDTO:
        review = self.render_review(authored_review.review)
        return replace(authored_review, review=review)

    def render_full_recipe(self, full_recipe: FullRecipeDTO) -> FullRecipeDTO:
        recipe = self.render_recipe(full_recipe.recipe)
        reviews = [self.render_authored_review(i) for i in full_recipe.reviews]
        return replace(full_recipe, recipe=recipe, reviews=reviews)
