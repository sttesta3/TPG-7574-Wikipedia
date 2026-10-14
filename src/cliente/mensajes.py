import socket
from collections import namedtuple

FIN_MENSAJE =  b'\x00'
DATA_MENSAJE =  b'\x01'

class DataMensaje:
    def __init__(self, row: namedtuple) -> None:
        self.resumen = str(row.abstract)
        self.fecha = row.date_modified.year
        self.imgUrl = "" if row.image == None else row.image["content_url"]
        self.lenguaje = 1 if row.in_language["identifier"] == "en" else 0
        self.seccion = row.sections
        self.nombre = row.name
    
    def _aBytes(self) -> bytes:
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


    def send(self, socket: socket) -> None:
        print(self._aBytes())



