import os
import socket
from safeSocket import safeSend, safeRecv

NOMBRE = os.environ["NOMBRE"]
LATIDOPORT = int(os.environ["LATIDOPORT"])

LATIDO_MENSAJE = b'\x01'

class latido():
    def __init__(self, pikaConnection) -> None:
        self.pikaConnection = pikaConnection
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    def start(self) -> None:
        self.socket.bind(("0.0.0.0", LATIDOPORT))
        self.socket.listen()
        while True:
            maestroSocket, _ = self.socket.accept()
            while True:
                try:
                    _ = safeRecv(maestroSocket, 1)
                    self.pikaConnection.add_callback_threadsafe(lambda: latir(maestroSocket))
                except Exception:
                    maestroSocket.close()
                    break
                

def latir(maestroSocket: socket.socket):
    safeSend(maestroSocket, LATIDO_MENSAJE)
