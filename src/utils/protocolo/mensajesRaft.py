import socket
from abc import ABC, abstractmethod
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
    def __init__(self, candidatoId: int = None, term: int = None, index: int = None ) -> None:
        self.candidatoId = candidatoId
        self.term = term
        self.index = index

    
    def aBytes(self) -> bytes:
        mensajeBytes = VOTACION_MENSAJE

        mensajeBytes += (12).to_bytes(4, byteorder="big")
        mensajeBytes += self.candidatoId.to_bytes(4, byteorder="big")
        mensajeBytes += self.term.to_bytes(4, byteorder="big")
        mensajeBytes += self.index.to_bytes(4, byteorder="big")

        return mensajeBytes
    

    def deBytes(self, bytes: bytes) -> None:
        totalLeido = 0

        self.candidatoId = int.from_bytes(bytes[totalLeido:totalLeido+4], byteorder="big")
        totalLeido += 4

        self.term = int.from_bytes(bytes[totalLeido:totalLeido+4], byteorder="big")
        totalLeido += 4

        self.index = int.from_bytes(bytes[totalLeido:totalLeido+4], byteorder="big")


class VotoMensaje(RaftMensaje):
    def __init__(self, voto: int = None, term: int = None) -> None:
        self.voto = voto
        self.term = term

    
    def aBytes(self) -> bytes:
        mensajeBytes = VOTO_MENSAJE

        mensajeBytes += (5).to_bytes(4, byteorder="big")
        mensajeBytes += self.voto.to_bytes(1, byteorder="big")
        mensajeBytes += self.term.to_bytes(4, byteorder="big")

        return mensajeBytes
    

    def deBytes(self, bytes: bytes) -> None:
        
        totalLeido = 0
        self.voto = int.from_bytes(bytes[totalLeido:totalLeido+1], byteorder="big")
        totalLeido += 1

        self.term = int.from_bytes(bytes[totalLeido:totalLeido+4], byteorder="big")



class LatidoMensaje(RaftMensaje):
    def __init__(self, data: MensajeSistema = None) -> None:
        self.data = data

    
    def aBytes(self) -> bytes:
        mensajeBytes = LATIDO_MENSAJE

        dataBytes = b''
        if self.data is not None and len(self.data) > 0:
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
    def __init__(self, liderId: int = None, term: int = None) -> None:
        self.liderId = liderId
        self.term = term

    def aBytes(self) -> bytes:
        mensajeBytes = LIDER_MENSAJE

        mensajeBytes += (8).to_bytes(4, byteorder="big")
        mensajeBytes += self.liderId.to_bytes(4, byteorder="big")
        mensajeBytes += self.term.to_bytes(4, byteorder="big")

        return mensajeBytes
    

    def deBytes(self, bytes: bytes) -> None:
        totalLeido = 0

        self.liderId = int.from_bytes(bytes[totalLeido:totalLeido+4], byteorder="big")
        totalLeido += 4

        self.term = int.from_bytes(bytes[totalLeido:totalLeido+4], byteorder="big")
    
      
async def obtenerRespuesta(reader, instancia: RaftMensaje) -> RaftMensaje:
    respuestaInfo = await reader.readexactly(4)
    respuestaSize = int.from_bytes(respuestaInfo, byteorder="big")

    if respuestaSize == 0:
        return instancia

    bytes = await reader.readexactly(respuestaSize)
    instancia.deBytes(bytes)

    return instancia


async def recvMensaje(reader) -> RaftMensaje:
    tipo = await reader.readexactly(1)


    if tipo == LIDER_MENSAJE:
        return await obtenerRespuesta(reader, LiderMensaje())
    if tipo == RESPUESTA_LATIDO_MENSAJE:
        return await obtenerRespuesta(reader, RespuestaLatidoMensaje())
    if tipo == LATIDO_MENSAJE:
        return await obtenerRespuesta(reader, LatidoMensaje())
    if tipo == VOTO_MENSAJE:
        return await obtenerRespuesta(reader, VotoMensaje())
    if tipo == VOTACION_MENSAJE:
        return await obtenerRespuesta(reader, VotacionMensaje())
    else:
        return None
        