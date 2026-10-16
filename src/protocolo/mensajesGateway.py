import socket
from abc import ABC, abstractmethod
from safeSocket import safeRecv, safeSend


RESPUESTA1_MENSAJE = b'\x01'
RESPUESTA2_MENSAJE = b'\x02'
RESPUESTA3_MENSAJE = b'\x03'
RESPUESTA4_MENSAJE = b'\x04'
RESPUESTA5_MENSAJE = b'\x05'

class Respuesta(ABC):
    @abstractmethod
    def aBytes(self) -> bytes:
        pass

    @abstractmethod
    def deBytes(self, bytes: bytes) -> None:
        pass

class Respuesta1Mensaje(Respuesta):

    def __init__(self, url: str = None, fecha: int = None) -> None:
        if url is None and fecha is None:
            return
        self.url = url
        self.fecha = fecha


    def aBytes(self) -> bytes:
        bytesMensaje = RESPUESTA1_MENSAJE

        urlBytes = self.url.encode("UTF-8")
        bytesMensaje += (len(urlBytes) + 6).to_bytes(4, byteorder="big")
        bytesMensaje += len(urlBytes).to_bytes(4, byteorder="big")
        bytesMensaje += urlBytes
        bytesMensaje += self.fecha.to_bytes(2, byteorder="big")

        return bytesMensaje
    
    
    def deBytes(self, bytes: bytes) -> None:
        totalLeido = 0
        
        urlLen = int.from_bytes(bytes[totalLeido:totalLeido+4], byteorder="big")
        self.url = bytes[totalLeido+4:totalLeido+urlLen+4].decode()
        totalLeido += (urlLen + 4)

        self.fecha = int.from_bytes(bytes[totalLeido:totalLeido+2], byteorder="big")


class Respuesta2Mensaje(Respuesta):

    def __init__(self, nombre: str = None, url: str = None, imgBytes: bytes = None) -> None:
        if nombre is None and url is None and imgBytes is None:
            return
        self.nombre = nombre
        self.url = url
        self.imgBytes = imgBytes


    def aBytes(self) -> bytes:
        bytesMensaje = RESPUESTA2_MENSAJE

        nombreBytes = self.nombre.encode("UTF-8")
        urlbytes = self.url.encode("UTF-8")

        tamañoMensaje = len(nombreBytes) + len(urlbytes) + len(self.imgBytes) + 12
        bytesMensaje += tamañoMensaje.to_bytes(4, byteorder="big")

        bytesMensaje += len(nombreBytes).to_bytes(4, byteorder="big")
        bytesMensaje += nombreBytes

        bytesMensaje += len(urlbytes).to_bytes(4, byteorder="big")
        bytesMensaje += urlbytes

        bytesMensaje += len(self.imgBytes).to_bytes(4, byteorder="big")
        bytesMensaje += self.imgBytes

        return bytesMensaje
    

    def deBytes(self, bytes: bytes) -> None:
        totalLeido = 0
        
        nombreTamaño = int.from_bytes(bytes[totalLeido:totalLeido+4], byteorder="big")
        self.nombre = bytes[totalLeido+4:totalLeido+nombreTamaño+4].decode()
        totalLeido += (nombreTamaño + 4)

        urlTamaño = int.from_bytes(bytes[totalLeido:totalLeido+4], byteorder="big")
        self.url = bytes[totalLeido+4:totalLeido+urlTamaño+4].decode()
        totalLeido += (urlTamaño + 4)

        imgBytesTamaño = int.from_bytes(bytes[totalLeido:totalLeido+4], byteorder="big")
        self.imgBytes = bytes[totalLeido+4:totalLeido+imgBytesTamaño+4]


class Respuesta3Mensaje(Respuesta):

    def __init__(self) -> None:
        pass

    def aBytes(self) -> bytes:
        pass

    def deBytes(self, bytes: bytes) -> None:        
        pass


class Respuesta4Mensaje(Respuesta):

    def __init__(self) -> None:
        pass

    def aBytes(self) -> bytes:
        pass

    def deBytes(self, bytes: bytes) -> None:        
        pass


class Respuesta5Mensaje(Respuesta):

    def __init__(self) -> None:
        pass

    def aBytes(self) -> bytes:
        pass

    def deBytes(self, bytes: bytes) -> None:        
        pass

def sendRespuesta(socket: socket.socket, respuesta: Respuesta) -> None:    
    safeSend(socket, respuesta.aBytes())

def obtenerRespuesta(socket: socket.socket, instancia: Respuesta) -> Respuesta:
    respuestaInfo = safeRecv(socket, 4)
    respuestaSize = int.from_bytes(respuestaInfo, byteorder="big")

    bytes = safeRecv(socket, respuestaSize)
    instancia.deBytes(bytes)

    return instancia

def recvMensaje(socket: socket.socket) -> Respuesta:
    type = safeRecv(socket, 1)

    if type == RESPUESTA1_MENSAJE:
        return obtenerRespuesta(socket, Respuesta1Mensaje())
    if type == RESPUESTA2_MENSAJE:
        return obtenerRespuesta(socket, Respuesta2Mensaje())
    else:
        return None