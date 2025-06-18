from collections.abc import Sequence
from typing import (
    TypeVar,
)

from sqlalchemy import Delete, Insert, Select, Update
from sqlalchemy.engine import Row
from sqlalchemy.sql.dml import (
    ReturningInsert,
    ReturningUpdate,
)

from infrastructure.sqlalchemy.models.base import Base
from infrastructure.sqlalchemy.transactions import SQLAlchemyTransactionManager


RESULT = TypeVar("RESULT", bound=Base)


class QueryExecutor:
    def __init__(self, transaction_manager: SQLAlchemyTransactionManager):
        self.transaction_manager = transaction_manager

    def execute_scalar_one(
        self,
        statement: (
            Select[tuple[RESULT]]
            | Insert[RESULT]
            | Update[RESULT]
            | Delete[RESULT]
            | ReturningInsert[tuple[RESULT]]
            | ReturningUpdate[tuple[RESULT]]
        ),
    ) -> RESULT | None:
        with self.transaction_manager.get_session():
            return self.execute(statement).scalar_one_or_none()

    def execute_scalar_many(
        self,
        statement: (
            Select[tuple[RESULT]]
            | Insert[RESULT]
            | Update[RESULT]
            | Delete[RESULT]
            | ReturningInsert[tuple[RESULT]]
            | ReturningUpdate[tuple[RESULT]]
        ),
    ) -> Sequence[RESULT]:
        with self.transaction_manager.get_session():
            return self.execute(statement).scalars().all()

    def execute_one(
        self,
        statement: Select[tuple[RESULT, ...]],
    ) -> Row[tuple[RESULT, ...]] | None:
        with self.transaction_manager.get_session():
            return self.execute(statement).one_or_none()

    def execute_many(
        self,
        statement: Select[tuple[RESULT, ...]],
    ) -> Sequence[Row[tuple[RESULT, ...]]]:
        with self.transaction_manager.get_session():
            return self.execute(statement).all()

    def execute(
        self,
        statement: (
            Select[tuple[RESULT, ...]]
            | Insert[RESULT]
            | Update[RESULT]
            | Delete[RESULT]
            | ReturningInsert[tuple[RESULT]]
            | ReturningUpdate[tuple[RESULT]]
        ),
    ):
        """
        Use is not recommended, prefer execute_scalar_one, execute_scalar_many, execute_one, or execute_many.
        Must be used inside a transaction context manager before session.close() is called.
        """
        with self.transaction_manager.get_session() as session:
            result = session.execute(statement)
            return result

    def add(
        self,
        model: Base,
    ) -> None:
        with self.transaction_manager.get_session() as session:
            session.add(model)
            session.flush()

    def add_all(
        self,
        models: Sequence[Base],
    ) -> None:
        with self.transaction_manager.get_session() as session:
            session.add_all(models)
            session.flush()

    def save(
        self,
        model: RESULT,
    ) -> RESULT:
        with self.transaction_manager.get_session() as session:
            model = session.merge(model)
            session.flush()
            return model
