import os
import sys

from infrastructure.app.app import App


print("CWD:", os.getcwd())
print("sys.path:", sys.path)
print("__package__:", __package__)
print("__name__:", __name__)


if __name__ == "__main__":
    application = App()
    application.configure()
    application.run()
