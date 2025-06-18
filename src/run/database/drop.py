from di.container import Container
from infrastructure.sqlalchemy.database import Database
from infrastructure.sqlalchemy.models.base import Base


def main():
    container = Container()
    container.init_resources()
    config = container.config()

    database = Database(config.DB)
    database.drop_database(Base.metadata)


if __name__ == "__main__":
    main()
