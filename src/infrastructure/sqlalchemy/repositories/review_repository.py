from collections.abc import Sequence
from datetime import datetime
from typing import cast

from sqlalchemy import select

from application.exceptions import NotFoundError
from domain.entities.entity import Id
from domain.entities.review.review import AuthoredReview, Review
from domain.entities.user.role import Role
from domain.entities.user.user import User
from domain.entities.user.value_objects import FullName
from domain.repositories.review_repository import IReviewRepository
from infrastructure.sqlalchemy.models.review import ReviewModel
from infrastructure.sqlalchemy.models.role import RoleModel
from infrastructure.sqlalchemy.models.user import UserModel
from infrastructure.sqlalchemy.query_executor import QueryExecutor
from infrastructure.sqlalchemy.transactions import SQLAlchemyTransactionManager


class SQLAlchemyReviewRepository(IReviewRepository):
    def __init__(
        self,
        query_executor: QueryExecutor,
        transaction_manager: SQLAlchemyTransactionManager,
    ):
        self.query_executor = query_executor
        self.transaction_manager = transaction_manager

    def get_by_id(self, review_id: int) -> Review:
        statement = select(ReviewModel).where(ReviewModel.id == review_id)
        review_model = self.query_executor.execute_scalar_one(statement)
        if not review_model:
            raise NotFoundError(review_id, "Review")
        return self._to_domain(review_model)

    def get_by_recipe_id(self, recipe_id: int) -> list[Review]:
        statement = select(ReviewModel).where(
            ReviewModel.recipe_id == recipe_id
        )
        review_models = self.query_executor.execute_scalar_many(statement)
        return [self._to_domain(model) for model in review_models]

    def get_with_author_by_recipe_id(
        self, recipe_id: int
    ) -> Sequence[AuthoredReview]:
        statement = (
            select(ReviewModel, UserModel, RoleModel)
            .join(UserModel, ReviewModel.user_id == UserModel.id)
            .join(RoleModel, UserModel.role_id == RoleModel.id)
            .where(ReviewModel.recipe_id == recipe_id)
        )
        result = self.query_executor.execute_many(statement)

        return [
            self._to_authored_review(
                row.ReviewModel, row.UserModel, row.RoleModel
            )
            for row in result
        ]

    def save(self, review: Review) -> Review:
        with self.transaction_manager.get_session():
            review_model = self._to_model(review)
            review_model = self.query_executor.save(review_model)
            return self._to_domain(review_model)

    def exists_for_user_and_recipe(self, user_id: int, recipe_id: int) -> bool:
        statement = select(ReviewModel).where(
            ReviewModel.user_id == user_id, ReviewModel.recipe_id == recipe_id
        )
        review_model = self.query_executor.execute_scalar_one(statement)
        return review_model is not None

    def _to_authored_review(
        self, review: ReviewModel, user: UserModel, role: RoleModel
    ) -> AuthoredReview:
        return AuthoredReview(
            review=self._to_domain(review),
            author=self._to_user_domain(user, role),
        )

    def _to_domain(self, model: ReviewModel) -> Review:
        return Review(
            entity_id=Id(cast(int, model.id)),
            recipe_id=Id(cast(int, model.recipe_id)),
            user_id=Id(cast(int, model.user_id)),
            rating=cast(int, model.rating),
            text=cast(str, model.text),
            created_at=cast(datetime, model.created_at),
        )

    def _to_user_domain(self, model: UserModel, role: RoleModel) -> User:
        return User(
            entity_id=Id(cast(int, model.id)),
            username=cast(str, model.username),
            password_hash=cast(str, model.password_hash),
            full_name=FullName(
                surname=cast(str, model.surname),
                name=cast(str, model.name),
                patronymic=cast(str, model.patronymic),
            ),
            role=(
                Role(
                    entity_id=Id(cast(int, role.id)),
                    name=cast(str, role.name),
                    description=cast(str, role.description),
                )
            ),
        )

    def _to_model(self, review: Review) -> ReviewModel:
        return ReviewModel(
            id=review.id.value if review.id else None,
            recipe_id=review.recipe_id.value,
            user_id=review.user_id.value,
            rating=review.rating,
            text=review.text,
            created_at=review.created_at,
        )
