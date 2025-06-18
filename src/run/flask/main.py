from infrastructure.app.app import App


if __name__ == "__main__":
    application = App()
    application.configure()
    application.run()
