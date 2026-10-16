import socket
from safeSocket import safeRecv, safeSend


QUERY1_MENSAJE = b'\x01'
QUERY2_MENSAJE = b'\x02'
QUERY3_MENSAJE = b'\x03'
QUERY4_MENSAJE = b'\x04'
QUERY5_MENSAJE = b'\x05'

class Query1Mensaje():

    def __init__(self, url: str = None, fecha: int = None) -> None:
        if url is None and fecha is None:
            return
        self.url = url
        self.fecha = fecha


    def aBytes(self) -> bytes:
        bytesMensaje = QUERY1_MENSAJE

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


    def send(self, socket: socket.socket) -> None:
        safeSend(socket, self.aBytes())


class Query2Mensaje():

    def __init__(self, nombre: str = None, url: str = None, imgBytes: bytes = None) -> None:
        if nombre is None and url is None and imgBytes is None:
            return
        self.nombre = nombre
        self.url = url
        self.imgBytes = imgBytes


    def aBytes(self) -> bytes:
        bytesMensaje = QUERY2_MENSAJE

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



def obtenerQuery(socket: socket.socket, instancia):
    queryInfo = safeRecv(socket, 4)
    querySize = int.from_bytes(queryInfo, byteorder="big")
    bytes = safeRecv(socket, querySize)
    instancia.deBytes(bytes)

    return instancia

def recvMensaje(socket: socket.socket):
    type = safeRecv(socket, 1)

    if type == QUERY1_MENSAJE:
        return obtenerQuery(socket, Query1Mensaje())
    if type == QUERY2_MENSAJE:
        return obtenerQuery(socket, Query2Mensaje())
    else:
        return None