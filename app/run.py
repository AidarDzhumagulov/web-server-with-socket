from app import App

SOCKET_HOST = "127.0.0.1"
SOCKET_PORT = 9999


if __name__ == '__main__':
    app_runner = App(SOCKET_HOST, SOCKET_PORT)
    with app_runner as app:
        app.run()
