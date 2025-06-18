import os
import sys


sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
)
print("CWD:", os.getcwd())
print("sys.path:", sys.path)
print("__package__:", __package__)
print("__name__:", __name__)


from infrastructure.app.app import App


if __name__ == "__main__":
    application = App()
    application.configure()
    application.run()
