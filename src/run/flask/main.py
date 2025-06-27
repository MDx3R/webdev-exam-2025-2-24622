from infrastructure.app.app import App


def create_app():
    _app = App()
    _app.configure()
    return _app


# Entry point
app = create_app().get_server()


if __name__ == "__main__":
    app.run()
