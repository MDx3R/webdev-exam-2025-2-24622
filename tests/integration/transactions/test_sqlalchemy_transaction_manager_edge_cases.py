from unittest.mock import MagicMock

import pytest

from application.exceptions import ApplicationError
from infrastrcuture.sqlalchemy.transactions import (
    SQLAlchemyTransactionManager,
)


class DummySession:
    def __init__(self, is_active: bool = True):
        self.is_active = is_active
        self.closed = False
        self.rolled_back = False
        self.committed = False

    def rollback(self):
        self.rolled_back = True

    def commit(self):
        if not self.is_active:
            self.rollback()
            raise ValueError("Session is inactive")
        self.committed = True

    def close(self):
        self.closed = True


class TestSQLAlchemyTransactionManagerEdgeCases:
    def setup_method(self):
        self.session_factory = MagicMock(return_value=DummySession())
        self.tm = SQLAlchemyTransactionManager(self.session_factory)

    def test_rollback_raises_if_no_session(self):
        with pytest.raises(ValueError, match="Session not found"):
            self.tm.rollback()

    def test_commit_raises_if_no_session(self):
        with pytest.raises(ValueError, match="Session not found"):
            self.tm.commit()

    def test_commit_raises_and_rolls_back_if_inactive(self):
        session = DummySession(is_active=False)
        self.tm._set_session(session)  # type: ignore
        with pytest.raises(ValueError, match="Session is inactive"):
            self.tm.commit()
        assert session.rolled_back

    def test_extract_duplicate_info_parses(self):
        err = Exception("DETAIL:  Key (username)=(john) already exists.")
        field, value = self.tm._extract_duplicate_info(err)  # type: ignore
        assert field == "username"
        assert value == "john"

    def test_extract_duplicate_info_returns_unknown(self):
        err = Exception("Some unrelated error")
        field, value = self.tm._extract_duplicate_info(err)  # type: ignore
        assert field == "unknown_field"
        assert value == "unknown_value"

    def test_handle_exception_reraises_application_error(self):
        err = ApplicationError("fail")
        with pytest.raises(ApplicationError):
            self.tm._handle_exception(err)  # type: ignore

    def test_handle_exception_reraises_other_exception(self):
        err = RuntimeError("fail")
        with pytest.raises(RuntimeError):
            self.tm._handle_exception(err)  # type: ignore

    def test_close_raises_if_no_session(self):
        with pytest.raises(ValueError, match="Session not found"):
            self.tm._close()  # type: ignore

    def test_close_closes_session(self):
        session = DummySession()
        self.tm._set_session(session)  # type: ignore
        self.tm._close()  # type: ignore
        assert session.closed
