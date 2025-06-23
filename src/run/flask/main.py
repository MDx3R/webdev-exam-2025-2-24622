from infrastructure.app.app import App


_app = App()
_app.configure()
app = _app.get_server()

if __name__ == "__main__":
    _app.run()
