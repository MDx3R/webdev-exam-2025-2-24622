from sqlalchemy import Engine, MetaData, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from infrastructure.config.config import DatabaseConfig


class Database:
    def __init__(self, config: DatabaseConfig):
        self.engine = self._create_engine(config)
        self.session_factory = self._create_session_factory()

    def _create_engine(self, config: DatabaseConfig) -> Engine:
        return create_engine(
            config.database_url, echo=False
        )  # флаг echo для подробных логов

    def _create_session_factory(self) -> sessionmaker[Session]:
        return sessionmaker(bind=self.engine, expire_on_commit=False)

    def get_engine(self) -> Engine:
        return self.engine

    def get_session_factory(self) -> sessionmaker[Session]:
        return self.session_factory

    def create_database(self, metadata: MetaData) -> None:
        metadata.create_all(self.engine)

    def drop_database(self, metadata: MetaData) -> None:
        metadata.drop_all(self.engine)

    def shutdown(self) -> None:
        if self.engine:
            self.engine.dispose()
