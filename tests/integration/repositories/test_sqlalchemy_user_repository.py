import pytest

from application.exceptions import NotFoundError
from domain.entities.entity import Id
from domain.entities.user.role import RoleEnum
from domain.entities.user.user import User
from domain.entities.user.value_objects import FullName
from infrastructure.sqlalchemy.repositories.user_repository import (
    SQLAlchemyUserRepository,
)
from infrastructure.sqlalchemy.transactions import SQLAlchemyTransactionManager


class Counter:
    counter = 0


class TestSQLAlchemyUserRepository:
    @pytest.fixture(autouse=True)
    def setup(
        self,
        user_repository: SQLAlchemyUserRepository,
        transaction_manager: SQLAlchemyTransactionManager,
    ):
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

    def test_get_by_id_success(self):
        user = self._get_user()
        saved_user = self.user_repository.save(user)

        retrieved_user = self.user_repository.get_by_id(
            saved_user.id_safe.value
        )

        assert retrieved_user is not None
        assert retrieved_user.username == user.username
        assert retrieved_user.full_name.surname == user.full_name.surname
        assert retrieved_user.role.name == user.role.name

    def test_get_by_id_not_found(self):
        with pytest.raises(NotFoundError, match="User"):
            self.user_repository.get_by_id(999)

    def test_get_by_username_success(self):
        user = self._get_user()
        saved_user = self.user_repository.save(user)

        retrieved_user = self.user_repository.get_by_username(
            saved_user.username
        )

        assert retrieved_user is not None
        assert retrieved_user.id == saved_user.id
        assert retrieved_user.username == user.username

    def test_get_by_username_not_found(self):
        with pytest.raises(NotFoundError, match="User"):
            self.user_repository.get_by_username("nonexistent")

    def test_exists_by_username_true(self):
        user = self._get_user()
        self.user_repository.save(user)

        exists = self.user_repository.exists_by_username(user.username)

        assert exists is True

    def test_exists_by_username_false(self):
        exists = self.user_repository.exists_by_username("nonexistent")

        assert exists is False

    def test_exists_true(self):
        user = self._get_user()
        self.user_repository.save(user)

        exists = self.user_repository.exists(user.id_safe.value)

        assert exists is True

    def test_exists_false(self):
        exists = self.user_repository.exists(999)

        assert exists is False

    def test_save_user_success(self):
        user = self._get_user()
        saved_user = self.user_repository.save(user)

        assert saved_user.id

        assert self.user_repository.exists_by_username(user.username)
        retrieved_user = self.user_repository.get_by_id(
            saved_user.id_safe.value
        )
        assert retrieved_user.username == user.username
        assert retrieved_user.full_name.name == user.full_name.name
        assert retrieved_user.role.name == user.role.name
