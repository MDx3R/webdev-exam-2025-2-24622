import re
from collections.abc import Generator
from contextlib import contextmanager
from contextvars import ContextVar

import psycopg2.errors
import sqlalchemy.exc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from application.exceptions import (
    ApplicationError,
    DuplicateEntryError,
    IntegrityError,
    RepositoryError,
)
from application.transactions.transaction_manager import ITransactionManager


class SQLAlchemyTransactionManager(ITransactionManager):
    def __init__(self, session_factory: sessionmaker[Session]):
        self.session_factory = session_factory
        self._current_session: ContextVar[Session | None] = ContextVar(
            "_current_session", default=None
        )

    def rollback(self):
        session = self._get_session()
        if not session:
            raise ValueError("Session not found")

        session.rollback()

    def commit(self):
        session = self._get_session()
        if not session:
            raise ValueError("Session not found")
        if not session.is_active:
            session.rollback()
            raise ValueError("Session is inactive")

        session.commit()

    def _extract_duplicate_info(self, error: BaseException) -> tuple[str, str]:
        match = re.search(r"\((\w+)\)=\((.*?)\)", str(error))
        if match:
            return match.group(1), match.group(2)
        return "unknown_field", "unknown_value"

    def _handle_exception(self, exception: BaseException):
        if isinstance(exception, ApplicationError):
            raise exception

        if isinstance(exception, sqlalchemy.exc.DatabaseError):
            if isinstance(exception.orig, psycopg2.errors.UniqueViolation):
                field, value = self._extract_duplicate_info(exception.orig)
                raise DuplicateEntryError(field, value) from exception
            raise IntegrityError() from exception

        if isinstance(exception, sqlalchemy.exc.SQLAlchemyError):
            raise RepositoryError(
                f"{exception}", cause=exception
            ) from exception

        raise exception

    def __enter__(self) -> "ITransactionManager":
        existing_session = self._get_session()
        if (
            not existing_session
        ):  # reuse old session since nested sessions are not supported
            session = self._create_session()
            self._set_session(session)
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object | None,
    ):
        has_error = exc_type is not None
        self._finalize_transaction(has_error)

        if has_error:
            self._handle_exception(exc_val)  # type: ignore

    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        """
        Контекстный менеджер для получения сессии.
        - Использует текущую сессию, если она есть.
        - Иначе создаёт временную, коммитит/откатывает и закрывает.
        """
        existing_session = self._get_session()
        if existing_session:
            yield existing_session
            return

        session = self._create_session()
        self._set_session(session)

        try:
            yield session
            self._finalize_transaction(has_error=False)
        except Exception as exc:
            self._finalize_transaction(has_error=True)
            self._handle_exception(exc)  # raises
            raise

    def _finalize_transaction(self, has_error: bool):
        session = self._get_session()
        if not session:
            return

        try:
            if has_error:
                self.rollback()
            else:
                self.commit()
        except Exception as exc:
            self._handle_exception(exc)
        finally:
            self._close()
            self._reset_session()

    def _close(self):
        session = self._get_session()
        if not session:
            raise ValueError("Session not found")

        session.close()
        del session

    def _create_session(self) -> Session:
        return self.session_factory()

    def _get_session(self) -> Session | None:
        return self._current_session.get()

    def _set_session(self, session: Session):
        self._current_session.set(session)

    def _reset_session(self):
        self._current_session.set(None)
