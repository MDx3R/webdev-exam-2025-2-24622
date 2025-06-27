from infrastructure.app.app import App


if __name__ == "__main__":
    _app = App()
    _app.configure()
    app = _app.get_server()
    _app.run()
