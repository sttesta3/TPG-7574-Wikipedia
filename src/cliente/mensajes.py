import ast
import socket
from safeSocket import safeSend, safeRecv
from collections import namedtuple

FIN_MENSAJE =  b'\x00'
DATA_MENSAJE =  b'\x01'
LOTE_MENSAJE = b'\x02'

def _seccionATexto(documento: str) -> str:
    textoSeccion = ""
    for seccion in ast.literal_eval(documento):
        try:
            for parrafo in seccion["has_parts"]:
                if parrafo["type"] == "paragraph":
                    textoSeccion += parrafo["value"] 
        except Exception:
            pass

    return textoSeccion


class DataMensaje:
        
    def __init__(self, fila: namedtuple = None) -> None:
        if fila is None:
            return
        self.url = fila.url
        self.resumen = str(fila.abstract)
        self.fecha = fila.date_modified.year
        self.imgUrl = "" if fila.image == None else fila.image["content_url"]
        self.lenguaje = 1 if fila.in_language["identifier"] == "en" else 0
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

        return bytesMensaje


    def deBytes(self, bytes: bytes) -> None:
        totalLeido = 0
        urlLen = int.from_bytes(bytes[totalLeido:4], byteorder="big")
        self.url = bytes[totalLeido+4:urlLen].decode()
        totalLeido += (urlLen + 4)

        resumenLen = int.from_bytes(bytes[totalLeido:4], byteorder="big")
        self.resumen = bytes[totalLeido+4:resumenLen].decode()
        totalLeido += (resumenLen + 4)

        self.fecha = int.from_bytes(bytes[totalLeido:2], byteorder="big")
        totalLeido += 2

        imgUrlLen = int.from_bytes(bytes[totalLeido:4], byteorder="big")
        self.imgUrl = bytes[totalLeido+4:imgUrlLen].decode()
        totalLeido += (imgUrlLen + 4)

        self.lenguaje = int.from_bytes(bytes[totalLeido:1], byteorder="big")
        totalLeido += 1

        seccionLen = int.from_bytes(bytes[totalLeido:4], byteorder="big")
        self.seccion = bytes[totalLeido+4:seccionLen].decode()
        totalLeido += (seccionLen + 4)

        nombreLen = int.from_bytes(bytes[totalLeido:4], byteorder="big")
        self.nombre = bytes[totalLeido+4:nombreLen].decode()


class FinMensaje():
    def __init__(self) -> None:
        pass
    

    def aBytes(self) -> bytes:
        return FIN_MENSAJE
        

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


    def aBytes(self) -> bytes:
        bytesMensaje = LOTE_MENSAJE
        bytesMensaje += len(self.lote).to_bytes(2, byteorder="big")
        
        dataMensajeBytes = b''
        for mensaje in self.lote:
            dataMensajeBytes += mensaje.aBytes()
        
        bytesMensaje += len(dataMensajeBytes).to_bytes(4, byteorder="big")
        bytesMensaje += dataMensajeBytes

        return bytesMensaje


    def deBytes(self, bytes) -> None:
        

    def obtenerLote(self) -> list[DataMensaje]:
        lote = self.lote
        self.lote = []
        return lote
