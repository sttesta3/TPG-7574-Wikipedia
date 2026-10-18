import ast
import socket
from safeSocket import safeSend, safeRecv
from collections import namedtuple

LENGUAJEINGLES = 1
LENGUAJEFRANCES = 1


FIN_MENSAJE =  b'\x00'
DATA_MENSAJE =  b'\x01'
LOTE_MENSAJE = b'\x02'

def _seccionATexto(documento: str) -> str:
    textoSeccion = ""
    try:
        for seccion in ast.literal_eval(documento):
            for parrafo in seccion["has_parts"]:
                if parrafo["type"] == "paragraph":
                    textoSeccion += parrafo["value"] 
    except Exception:
        pass

    return textoSeccion


class DataMensaje():
    def __init__(self, fila: namedtuple = None) -> None:
        if fila is None:
            return
        self.url = fila.url
        self.resumen = str(fila.abstract)
        self.fecha = fila.date_modified.year
        self.imgUrl = "" if fila.image == None else fila.image["content_url"]
        self.lenguaje = LENGUAJEINGLES if fila.in_language["identifier"] == "en" else LENGUAJEFRANCES
        self.seccion = _seccionATexto(fila.sections)
        self.nombre = fila.name
    

    def aBytes(self) -> bytes:
        urlBytes = self.url.encode("UTF-8")
        resumenBytes = self.resumen.encode("UTF-8")
        imgUrlBytes = self.imgUrl.encode("UTF-8")
        seccionBytes = self.seccion.encode("UTF-8")
        nombreBytes = self.nombre.encode("UTF-8")

        bytesMensaje = DATA_MENSAJE

        tamañoMensaje = len(resumenBytes) + len(imgUrlBytes) + len(seccionBytes) + len(nombreBytes) + len(urlBytes)
        bytesMensaje += (tamañoMensaje  + 20 + 3).to_bytes(4, byteorder="big")
        
        bytesMensaje += len(urlBytes).to_bytes(4, byteorder="big")
        bytesMensaje += urlBytes

        bytesMensaje += len(resumenBytes).to_bytes(4, byteorder="big")
        bytesMensaje += resumenBytes

        bytesMensaje += self.fecha.to_bytes(2, byteorder="big")

        bytesMensaje += len(imgUrlBytes).to_bytes(4, byteorder="big")
        bytesMensaje += imgUrlBytes

        bytesMensaje += self.lenguaje.to_bytes(1, byteorder="big")

        bytesMensaje += len(seccionBytes).to_bytes(4, byteorder="big")
        bytesMensaje += seccionBytes

        bytesMensaje += len(nombreBytes).to_bytes(4, byteorder="big")
        bytesMensaje += nombreBytes

        print(tamañoMensaje)

        return bytesMensaje


    def deBytes(self, bytes: bytes) -> None:
        totalLeido = 0
        urlLen = int.from_bytes(bytes[totalLeido:totalLeido+4], byteorder="big")
        print(urlLen)

        self.url = bytes[totalLeido+4:totalLeido+urlLen].decode()
        totalLeido += (urlLen + 4)

        resumenLen = int.from_bytes(bytes[totalLeido:totalLeido+4], byteorder="big")
        self.resumen = bytes[totalLeido+4:totalLeido+resumenLen+4].decode()
        totalLeido += (resumenLen + 4)

        self.fecha = int.from_bytes(bytes[totalLeido:totalLeido+2], byteorder="big")
        totalLeido += 2

        imgUrlLen = int.from_bytes(bytes[totalLeido:totalLeido+4], byteorder="big")
        self.imgUrl = bytes[totalLeido+4:totalLeido+imgUrlLen+4].decode()
        totalLeido += (imgUrlLen + 4)

        self.lenguaje = int.from_bytes(bytes[totalLeido:totalLeido+1], byteorder="big")
        totalLeido += 1

        seccionLen = int.from_bytes(bytes[totalLeido:totalLeido+4], byteorder="big")
        self.seccion = bytes[totalLeido+4:totalLeido+seccionLen+4].decode()
        totalLeido += (seccionLen + 4)

        nombreLen = int.from_bytes(bytes[totalLeido:totalLeido+4], byteorder="big")
        self.nombre = bytes[totalLeido+4:totalLeido+nombreLen+4].decode()


    def obtenerData(self, socket: socket.socket):
        dataInfo = safeRecv(socket, 4)
        dataSize = int.from_bytes(dataInfo[0:4], byteorder="big")

        bytes = safeRecv(socket, dataSize)

        self.deBytes(bytes)

        return self


class FinMensaje():
    def __init__(self, socket: socket.socket) -> None:
        self.socket = socket
    

    def aBytes(self) -> bytes:
        return FIN_MENSAJE
        
    
    def send(self) -> None:
        safeSend(self.socket, FIN_MENSAJE)


class LoteMensaje():
    def __init__(self, socket: socket = None, tamañoLote: int = None) -> None:
        self.tamañoLote = tamañoLote
        self.lote = []
        self.socket = socket


    def agregarMensaje(self, fila: namedtuple) -> None:
        self.lote.append(DataMensaje(fila))

        if len(self.lote) == self.tamañoLote:
            self.send()
            self.lote = []


    def aBytes(self) -> bytes:
        bytesMensaje = LOTE_MENSAJE
        bytesMensaje += len(self.lote).to_bytes(2, byteorder="big")
        
        dataMensajeBytes = b''
        for mensaje in self.lote:
            dataMensajeBytes += mensaje.aBytes()
        
        bytesMensaje += len(dataMensajeBytes).to_bytes(4, byteorder="big")
        bytesMensaje += dataMensajeBytes

        return bytesMensaje


    def deBytes(self, bytes: bytes, loteLen: int) -> None:
        totalLeido = 0
        
        for _ in range(loteLen):
            tamañoMensaje = int.from_bytes(bytes[totalLeido+1:totalLeido+5], byteorder="big")
            msg = DataMensaje()
            msg.deBytes(bytes[totalLeido+5:totalLeido+tamañoMensaje+5])
            self.lote.append(msg)
            totalLeido += tamañoMensaje + 5


    def obtenerLote(self) -> list[DataMensaje]:
        loteInfo = safeRecv(self.socket, 6)
        loteLen = int.from_bytes(loteInfo[0:2], byteorder="big")
        loteSize = int.from_bytes(loteInfo[2:6], byteorder="big")

        bytes = safeRecv(self.socket, loteSize)
        self.deBytes(bytes, loteLen)

        return self.lote
    

    def send(self) -> None:
        if len(self.lote) == 0:
            return

        mensaje = self.aBytes()
        safeSend(self.socket, mensaje)


def recvMensaje(socket: socket.socket) -> list[DataMensaje]:
    type = safeRecv(socket, 1)

    if type == FIN_MENSAJE: 
        return None
    elif type == LOTE_MENSAJE:
        return LoteMensaje(socket).obtenerLote()
    elif type == DATA_MENSAJE:
        return [DataMensaje.obtenerData(socket)]
    else:
        return None