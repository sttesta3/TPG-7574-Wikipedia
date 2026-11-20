import os
import socket
from safeSocket import safeSend
from protocolo.mensajesLatido import ConeccionMensaje, LatidoMensaje, recvMensaje


NOMBRE = os.environ["NOMBRE"]
MAESTROHOSTS = os.environ["MAESTROHOSTS"]
MAESTROPORT = int(os.environ["MAESTROPORT"])

class latido():
    def __init__(self, pikaConnection) -> None:
        self.pikaConnection = pikaConnection
        self.maestro = None

        self.conectarMaestro()

    def conectarMaestro(self) -> None:
        hosts = MAESTROHOSTS.split(",")
        while self.maestro is None:
            for host in hosts:
                if host is not None and host != "":
                    try:
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        sock.connect((host, MAESTROPORT)) 
                        self.maestro = sock
                        safeSend(self.maestro, ConeccionMensaje(NOMBRE))
                    except Exception:
                        continue


    def start(self) -> None:
        while True:
            try:
                _ = recvMensaje(self.maestro)
                self.pikaConnection.add_callback_threadsafe(lambda: latir(self.maestro))
            except (socket.error, OSError) :
                # murio el maestro, trato de conectarme a otro 
                self.maestro = None
                self.conectarMaestro()
            except Exception:
                continue
                

def latir(maestro: socket.socket):

    safeSend(maestro, LatidoMensaje(NOMBRE))
