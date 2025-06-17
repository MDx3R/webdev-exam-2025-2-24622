from application.commands.review.create_review_command import (
    CreateReviewCommand,
)
from application.dtos.review.review_dto import ReviewDTO
from application.dtos.user.user_descriptor import UserDescriptor
from application.interfaces.usecases.review.create_review_usecase import (
    ICreateReviewUseCase,
)
from application.transactions.transactional import transactional
from domain.entities.review.dtos import ReviewData
from domain.entities.review.factories import IReviewFactory
from domain.entities.user.role import RoleEnum
from domain.repositories.recipe_repository import IRecipeRepository
from domain.repositories.review_repository import IReviewRepository


class CreateReviewUseCase(ICreateReviewUseCase):
    def __init__(
        self,
        review_factory: IReviewFactory,
        recipe_repository: IRecipeRepository,
        review_repository: IReviewRepository,
    ):
        self.review_factory = review_factory
        self.recipe_repository = recipe_repository
        self.review_repository = review_repository

    @transactional
    def execute(
        self, command: CreateReviewCommand, descriptor: UserDescriptor
    ) -> ReviewDTO:
        if descriptor.role not in [RoleEnum.ADMIN.value, RoleEnum.USER.value]:
            raise PermissionError("User cannot create reviews.")

        if self.review_repository.exists_for_user_and_recipe(
            command.user_id, command.recipe_id
        ):
            raise ValueError("User has already reviewed this recipe.")

        review = self.review_factory.create(
            ReviewData(
                recipe_id=command.recipe_id,
                user_id=command.user_id,
                rating=command.rating,
                text=command.text,
            )
        )

        review = self.review_repository.save(review)
        return ReviewDTO.from_domain(review)
