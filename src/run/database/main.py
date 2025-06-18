from di.container import Container
from infrastructure.sqlalchemy.database import Database
from infrastructure.sqlalchemy.initializer.user_initializer import create_users


def main():
    container = Container()
    container.init_resources()
    config = container.config()

    database = Database(config.DB)
    create_users(database.get_session_factory()(), container.password_hasher())


if __name__ == "__main__":
    main()
