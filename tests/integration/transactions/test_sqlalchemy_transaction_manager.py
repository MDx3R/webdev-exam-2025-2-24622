from typing import Self

import pytest
import sqlalchemy
import sqlalchemy.exc
from sqlalchemy.orm.session import Session

from application.exceptions import ApplicationError
from application.transactions import transactional
from domain.entities.entity import Id
from domain.entities.user.role import RoleEnum
from domain.entities.user.user import User
from domain.entities.user.value_objects import FullName
from infrastrcuture.sqlalchemy.repositories.user_repository import (
    SQLAlchemyUserRepository,
)
from infrastrcuture.sqlalchemy.transactions import SQLAlchemyTransactionManager


class Counter:
    counter = 0


class TestSQLAlchemyTransactionManager:
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

    def _is_user_saved(self, user: User) -> bool:
        return self.user_repository.exists_by_username(user.username)

    def _create_user(self, user: User) -> User:
        return self.user_repository.save(user)

    def _get_session(self) -> Session | None:
        return self.transaction_manager._current_session.get()  # type: ignore

    def test_transaction_commit(self):
        user = self._get_user()
        with self.transaction_manager:
            result = self._create_user(user)

        assert result is not None
        assert result.username == user.username
        assert self._is_user_saved(user)

    def test_transaction_wihtout_transaction_manager(self):
        user = self._get_user()
        result = self.user_repository.save(user)

        assert result is not None
        assert result.username == user.username
        assert self._is_user_saved(user)

    def test_transaction_rollback(self):
        user = self._get_user()
        with pytest.raises(ValueError, match="Test rollback"):
            print("begin")
            with self.transaction_manager:
                self._create_user(user)
                print("raise")
                raise ValueError("Test rollback")

        assert not self._is_user_saved(user)

    def test_nested_transaction_is_shared(self):
        with self.transaction_manager as outer_session:
            with self.transaction_manager as inner_session:
                assert id(outer_session) == id(inner_session)

    def test_consecutive_transactions_not_shared(self):
        with self.transaction_manager:
            session1 = self._get_session()
        with self.transaction_manager:
            session2 = self._get_session()
        assert id(session1) != id(session2)

    def test_session_cleared_on_commit(self):
        with self.transaction_manager:
            assert self._get_session() is not None
        assert self._get_session() is None

    def test_session_cleared_on_rollback(self):
        with pytest.raises(ValueError, match="Test rollback"):
            with self.transaction_manager:
                assert self._get_session() is not None
                raise ValueError("Test rollback")
        assert self._get_session() is None

    def test_transactional_commit(self):
        user = self._get_user()

        @transactional
        def func(self: Self) -> User:
            return self._create_user(user)

        result = func(self)
        assert result is not None
        assert result.username == user.username
        assert self._is_user_saved(user)

    def test_transactional_rollback(self):
        user = self._get_user()

        @transactional
        def func(self: Self) -> User:
            self._create_user(user)
            raise ValueError("Test rollback")

        with pytest.raises(ValueError, match="Test rollback"):
            func(self)
        assert not self._is_user_saved(user)

    def test_transactional_creates_session(self):
        @transactional
        def func(self: Self):
            assert self._get_session() is not None

        func(self)

    def test_transactional_shares_transaction(self):
        @transactional
        def func(self: Self):
            outer = self._get_session()
            with self.transaction_manager:
                assert id(outer) == id(self._get_session())

        func(self)

    def test_applicaion_exception_raises(self):
        with pytest.raises(ApplicationError, match="Some error"):
            with self.transaction_manager:
                raise ApplicationError("Some error")

    def test_infrasturcture_exception_wraps_and_raises(self):
        with pytest.raises(ApplicationError, match=r".*Db unavailable.*"):
            with self.transaction_manager:
                raise sqlalchemy.exc.SQLAlchemyError("Db unavailable")
