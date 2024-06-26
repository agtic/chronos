from .socketIO_client import SocketIO

socketIO = SocketIO("localhost", 8000, transports=["xhr-polling"])


def send(message):
    socketIO.emit("backend", message)
    socketIO.wait(seconds=1)
