from datetime import datetime

import pytest

from application.exceptions import NotFoundError
from domain.entities.entity import Id
from domain.entities.review.review import Review
from domain.entities.user.role import RoleEnum
from domain.entities.user.user import User
from domain.entities.user.value_objects import FullName
from infrastructure.sqlalchemy.repositories.review_repository import (
    SQLAlchemyReviewRepository,
)
from infrastructure.sqlalchemy.repositories.user_repository import (
    SQLAlchemyUserRepository,
)
from infrastructure.sqlalchemy.transactions import SQLAlchemyTransactionManager


class Counter:
    counter = 0


class TestSQLAlchemyReviewRepository:
    @pytest.fixture(autouse=True)
    def setup(
        self,
        review_repository: SQLAlchemyReviewRepository,
        user_repository: SQLAlchemyUserRepository,
        transaction_manager: SQLAlchemyTransactionManager,
    ):
        self.review_repository = review_repository
        self.user_repository = user_repository
        self.transaction_manager = transaction_manager

    def _get_user(self) -> User:
        Counter.counter += 1
        return User(
            entity_id=Id(Counter.counter),
            username=f"username{Counter.counter}",
            full_name=FullName(surname="Doe", name="John", patronymic=None),
            password_hash="hash",
            role=RoleEnum.USER.value,
        )

    def _get_review(self, user_id: int, recipe_id: int) -> Review:
        Counter.counter += 1
        return Review(
            entity_id=Id(Counter.counter),
            recipe_id=Id(recipe_id),
            user_id=Id(user_id),
            rating=5,
            text="Great recipe!",
            created_at=datetime.now(),
        )

    def test_get_by_id_success(self):
        user = self._get_user()
        with self.transaction_manager:
            saved_user = self.user_repository.save(user)
            review = self._get_review(saved_user.id_safe.value, 1)
            saved_review = self.review_repository.save(review)

        with self.transaction_manager:
            retrieved_review = self.review_repository.get_by_id(
                saved_review.id_safe.value
            )

        assert retrieved_review is not None
        assert retrieved_review.rating == review.rating
        assert retrieved_review.text == review.text

    def test_get_by_id_not_found(self):
        with self.transaction_manager:
            with pytest.raises(NotFoundError, match="Review"):
                self.review_repository.get_by_id(999)

    def test_get_by_recipe_id_success(self):
        user = self._get_user()
        recipe_id = 1
        with self.transaction_manager:
            saved_user = self.user_repository.save(user)
            review1 = self._get_review(saved_user.id_safe.value, recipe_id)
            review2 = self._get_review(saved_user.id_safe.value, recipe_id)
            self.review_repository.save(review1)
            self.review_repository.save(review2)

        with self.transaction_manager:
            reviews = self.review_repository.get_by_recipe_id(recipe_id)

        assert len(reviews) == 2
        assert all(r.recipe_id.value == recipe_id for r in reviews)

    def test_get_by_recipe_id_empty(self):
        with self.transaction_manager:
            reviews = self.review_repository.get_by_recipe_id(999)

        assert len(reviews) == 0

    def test_get_with_author_by_recipe_id_success(self):
        user = self._get_user()
        print(user)
        recipe_id = 1
        with self.transaction_manager:
            saved_user = self.user_repository.save(user)
            review = self._get_review(saved_user.id_safe.value, recipe_id)
            self.review_repository.save(review)

        with self.transaction_manager:
            authored_reviews = (
                self.review_repository.get_with_author_by_recipe_id(recipe_id)
            )

        assert len(authored_reviews) == 1
        assert authored_reviews[0].author.username == user.username
        assert authored_reviews[0].review.recipe_id.value == recipe_id

    def test_exists_for_user_and_recipe_true(self):
        user = self._get_user()
        recipe_id = 1
        with self.transaction_manager:
            saved_user = self.user_repository.save(user)
            review = self._get_review(saved_user.id_safe.value, recipe_id)
            self.review_repository.save(review)

        with self.transaction_manager:
            exists = self.review_repository.exists_for_user_and_recipe(
                saved_user.id_safe.value, recipe_id
            )

        assert exists is True

    def test_exists_for_user_and_recipe_false(self):
        with self.transaction_manager:
            exists = self.review_repository.exists_for_user_and_recipe(
                999, 999
            )

        assert exists is False

    def test_save_review_success(self):
        user = self._get_user()
        recipe_id = 1
        with self.transaction_manager:
            saved_user = self.user_repository.save(user)
            review = self._get_review(saved_user.id_safe.value, recipe_id)
            saved_review = self.review_repository.save(review)

        with self.transaction_manager:
            retrieved_review = self.review_repository.get_by_id(
                saved_review.id_safe.value
            )
            assert retrieved_review.rating == review.rating
            assert retrieved_review.text == review.text
            assert retrieved_review.user_id == saved_user.id
