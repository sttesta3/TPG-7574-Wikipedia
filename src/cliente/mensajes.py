from safeSocket import safeSend, safeRecv
import socket
from collections import namedtuple

FIN_MENSAJE =  b'\x00'
DATA_MENSAJE =  b'\x01'
LOTE_MENSAJE = b'\x02'

class DataMensaje:
    def __init__(self, fila: namedtuple) -> None:
        self.resumen = str(fila.abstract)
        self.fecha = fila.date_modified.year
        self.imgUrl = "" if fila.image == None else fila.image["content_url"]
        self.lenguaje = 1 if fila.in_language["identifier"] == "en" else 0
        self.seccion = str(fila.sections)
        self.nombre = fila.name
    

    def aBytes(self) -> bytes:
        resumenBytes = self.resumen.encode("UTF-8")
        imgUrlBytes = self.imgUrl.encode("UTF-8")
        seccionBytes = self.seccion.encode("UTF-8")
        nombreBytes = self.nombre.encode("UTF-8")

        bytesMensaje = DATA_MENSAJE

        tamañoMensaje = len(resumenBytes) + len(imgUrlBytes) + len(seccionBytes) + len(nombreBytes)
        bytesMensaje += (tamañoMensaje  + 16 + 3).to_bytes(4, byteorder="big")
        
        bytesMensaje += len(resumenBytes).to_bytes(4, byteorder="big")
        bytesMensaje += resumenBytes
        bytesMensaje += self.fecha.to_bytes(2, byteorder="big")
        bytesMensaje += len(imgUrlBytes).to_bytes(4, byteorder="big")
        bytesMensaje += imgUrlBytes
        bytesMensaje += self.lenguaje.to_bytes(1, byteorder="big")
        bytesMensaje += len(seccionBytes).to_bytes(4, byteorder="big")
        bytesMensaje += seccionBytes
        bytesMensaje += len(nombreBytes).to_bytes(4, byteorder="big") # Se podria analizar la seccion y reducir la cantidad de info y poner solo los textos
        bytesMensaje += nombreBytes

        return bytesMensaje


    def send(self, socket: socket.socket) -> None:
        print(self.aBytes())
        safeSend(self.aBytes())


class FinMensaje():
    def __init__(self) -> None:
        pass
    

    def send(self, socket: socket.socket) -> None:
        socket.send(FIN_MENSAJE)

class LoteMensaje():
    def __init__(self, tamañoLote: int, socket: socket.socket) -> None:
        self.tamañoLote = tamañoLote
        self.lote = []
        self.socket = socket


    def agregarMensaje(self, fila: namedtuple) -> None:
        self.lote.append(DataMensaje(fila))

        if len(self.lote) == self.tamañoLote:
            self.send()
            self.lote = []


    def _aBytes(self) -> bytes:
        bytesMensaje = LOTE_MENSAJE
        bytesMensaje += len(self.lote).to_bytes(2, byteorder="big")
        
        dataMensajeBytes = b''
        for mensaje in self.lote:
            dataMensajeBytes += mensaje.aBytes()
        
        bytesMensaje += len(dataMensajeBytes).to_bytes(4, byteorder="big")
        bytesMensaje += dataMensajeBytes

        return bytesMensaje


    def send(self) -> None:
        if len(self.lote) == 0:
            return

        mensaje = self._aBytes()
        safeSend(self.socket, mensaje)