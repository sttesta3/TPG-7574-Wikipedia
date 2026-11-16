import socket
from abc import ABC, abstractmethod
from socket.safeSocket import safeRecv, safeSend
from protocolo.mensajesSistema import MensajeSistema, recvMensajeSistema

VOTACION_MENSAJE = b'\x01'
VOTO_MENSAJE = b'\x02'
LATIDO_MENSAJE = b'\x03'
RESPUESTA_LATIDO_MENSAJE = b'\x04'
LIDER_MENSAJE = b'\x05'

class RaftMensaje(ABC):
    @abstractmethod
    def aBytes(self) -> bytes:
        pass

    @abstractmethod
    def deBytes(self, bytes: bytes) -> None:
        pass


class VotacionMensaje(RaftMensaje):
    def __init__(self, candidatoId: int = None) -> None:
        self.candidatoId = candidatoId

    
    def aBytes(self) -> bytes:
        mensajeBytes = VOTACION_MENSAJE

        mensajeBytes += (4).to_bytes(4, byteorder="big")
        mensajeBytes += self.candidatoId.to_bytes(4, byteorder="big")

        return mensajeBytes
    

    def deBytes(self, bytes: bytes) -> None:
        
        self.candidatoId = int.from_bytes(bytes, byteorder="big")


class VotoMensaje(RaftMensaje):
    def __init__(self, voto: int = None) -> None:
        self.voto = voto

    
    def aBytes(self) -> bytes:
        mensajeBytes = VOTO_MENSAJE

        mensajeBytes += (1).to_bytes(4, byteorder="big")
        mensajeBytes += self.voto.to_bytes(1, byteorder="big")

        return mensajeBytes
    

    def deBytes(self, bytes: bytes) -> None:
        
        self.voto = int.from_bytes(bytes, byteorder="big")
        

class LatidoMensaje(RaftMensaje):
    def __init__(self, data: MensajeSistema = None) -> None:
        self.data = data

    
    def aBytes(self) -> bytes:
        mensajeBytes = LATIDO_MENSAJE

        dataBytes = b''
        if self.data is not None:
            dataBytes = self.data.aBytes()
        
        mensajeBytes += len(dataBytes).to_bytes(4, byteorder="big")
        mensajeBytes += dataBytes

        return mensajeBytes
    
    def deBytes(self, bytes: bytes) -> None:
        self.data = recvMensajeSistema(bytes)


class RespuestaLatidoMensaje(RaftMensaje):
    def __init__(self) -> None:
        return


    def aBytes(self) -> bytes:
        mensajeBytes = RESPUESTA_LATIDO_MENSAJE

        mensajeBytes += (0).to_bytes(4, byteorder="big")

        return mensajeBytes
    

    def deBytes(self, bytes: bytes) -> None:
        return None


class LiderMensaje(RaftMensaje):
    def __init__(self, liderId: int) -> None:
        self.liderId = liderId

    def aBytes(self) -> bytes:
        mensajeBytes = LIDER_MENSAJE

        mensajeBytes += (4).to_bytes(4, byteorder="big")
        mensajeBytes += self.liderId.to_bytes(4, byteorder="big")

        return mensajeBytes
    

    def deBytes(self, bytes: bytes) -> None:
        
        self.liderId = int.from_bytes(bytes, byteorder="big")
    
      
def obtenerRespuesta(socket: socket.socket, instancia: RaftMensaje) -> RaftMensaje:
    respuestaInfo = safeRecv(socket, 4)
    respuestaSize = int.from_bytes(respuestaInfo, byteorder="big")

    if len(respuestaSize) == 0:
        return instancia

    bytes = safeRecv(socket, respuestaSize)
    instancia.deBytes(bytes)

    return instancia


def recvMensaje(socket: socket.socket) -> RaftMensaje:
    type = safeRecv(socket, 1)

    if type == LIDER_MENSAJE:
        return obtenerRespuesta(socket, LiderMensaje())
    if type == RESPUESTA_LATIDO_MENSAJE:
        return obtenerRespuesta(socket, RespuestaLatidoMensaje())
    if type == LATIDO_MENSAJE:
        return obtenerRespuesta(socket, LatidoMensaje())
    if type == VOTO_MENSAJE:
        return obtenerRespuesta(socket, VotoMensaje())
    if type == VOTACION_MENSAJE:
        return obtenerRespuesta(socket, VotacionMensaje())
    else:
        return None
        