from application.transactions.configuration import CurrentTransactionManager
from di.container import Container
from infrastructure.config.config import BASE_FILE_DIR
from infrastructure.server.flask.app import FlaskServer
from infrastructure.sqlalchemy.database import Database


class App:
    def __init__(self) -> None:
        self.container = Container()
        self.container.init_resources()
        self.config = self.container.config()

        self.database = Database(self.config.DB)
        self.server = FlaskServer(
            BASE_FILE_DIR, self.container, self.config.AUTH
        )

    def configure(self):
        CurrentTransactionManager.set(self.container.transaction_manager())

        self.server.configure()
        self.server.setup_routes()

    def shutdown(self):
        self.database.shutdown()

    def run(self):
        self.server.app.run()
        self.database.shutdown()

    def get_server(self):
        return self.server.app
