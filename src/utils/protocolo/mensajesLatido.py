import socket
from safeSocket import safeRecv


CONECCION_MENSAJE = b'\x01'
LATIDO_MENSAJE = b'\x02'

class ConeccionMensaje():
    def __init__(self, nombre: str = None) -> None:
        self.nombre = nombre

    
    def aBytes(self) -> bytes:
        mensajeBytes = CONECCION_MENSAJE

        nombreBytes = self.nombre.encode("UTF-8")

        mensajeBytes += len(nombreBytes).to_bytes(4, byteorder="big")
        mensajeBytes += nombreBytes

        return mensajeBytes


    def deBytes(self, bytes: bytes) -> None:
        self.nombre = bytes.decode()


class LatidoMensaje():
    def __init__(self, nombre: str = None) -> None:
        self.nombre = nombre

    
    def aBytes(self) -> bytes:
        mensajeBytes = LATIDO_MENSAJE

        nombreBytes = self.nombre.encode("UTF-8")
        mensajeBytes += len(nombreBytes).to_bytes(4, byteorder="big")
        mensajeBytes += nombreBytes

        return mensajeBytes


    def deBytes(self, bytes: bytes) -> None:
        self.nombre = bytes.decode()


def recvMensaje(socket: socket.socket) -> (LatidoMensaje | ConeccionMensaje):
    info = safeRecv(socket, 5)

    type = info[0]
    msgSize = int.from_bytes(info[1:] , byteorder="big")

    msgBytes = safeRecv(socket, msgSize)
    msg = LatidoMensaje() if type == LATIDO_MENSAJE else ConeccionMensaje()
    msg.deBytes(msgBytes)

    return msg