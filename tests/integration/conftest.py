import pytest
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from application.transactions.configuration import CurrentTransactionManager
from infrastructure.config.config import Config
from infrastructure.sqlalchemy.database import Database
from infrastructure.sqlalchemy.initializer.initializer import initialize_data
from infrastructure.sqlalchemy.models.base import Base
from infrastructure.sqlalchemy.query_executor import QueryExecutor
from infrastructure.sqlalchemy.repositories.recipe_repository import (
    SQLAlchemyRecipeRepository,
)
from infrastructure.sqlalchemy.repositories.review_repository import (
    SQLAlchemyReviewRepository,
)
from infrastructure.sqlalchemy.repositories.user_repository import (
    SQLAlchemyUserRepository,
)
from infrastructure.sqlalchemy.transactions import SQLAlchemyTransactionManager


@pytest.fixture(scope="session")
def config():
    return Config.load_from_path("config/test_config.yaml")


@pytest.fixture(scope="session")
def database(config: Config):
    db = Database(config.DB)
    return db


@pytest.fixture(autouse=True)
def init(database: Database):
    database.create_database(Base.metadata)
    with database.get_session_factory()() as session:
        initialize_data(session)
    yield
    database.drop_database(Base.metadata)


@pytest.fixture(scope="session")
def session_factory(database: Database):
    return database.get_session_factory()


@pytest.fixture(scope="session")
def transaction_manager(session_factory: sessionmaker[Session]):
    manager = SQLAlchemyTransactionManager(session_factory)
    CurrentTransactionManager.set(manager)
    return manager


@pytest.fixture(scope="session")
def query_executor(transaction_manager: SQLAlchemyTransactionManager):
    return QueryExecutor(transaction_manager)


@pytest.fixture(scope="session")
def user_repository(
    query_executor: QueryExecutor,
    transaction_manager: SQLAlchemyTransactionManager,
):
    return SQLAlchemyUserRepository(query_executor, transaction_manager)


@pytest.fixture(scope="session")
def recipe_repository(
    query_executor: QueryExecutor,
    transaction_manager: SQLAlchemyTransactionManager,
):
    return SQLAlchemyRecipeRepository(query_executor, transaction_manager)


@pytest.fixture(scope="session")
def review_repository(
    query_executor: QueryExecutor,
    transaction_manager: SQLAlchemyTransactionManager,
):
    return SQLAlchemyReviewRepository(query_executor, transaction_manager)
