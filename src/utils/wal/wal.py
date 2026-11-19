import os
import uuid
from collections.abc import Iterator
from protocolo.mensajesSistema import MensajeSistema

class Wal():
    def __init__(self) -> None:
        self.logs = {}


    def guardarMensaje(self, mensaje: bytes, clienteId: uuid.UUID) -> None:
        if clienteId not in self.logs:
            self.logs[clienteId] = open("log/"+str(clienteId), "ab")

        self.logs[clienteId].write(mensaje.aBytes() + b"\n")


    def recuperarLogs(self) -> Iterator[bytes]:
        logsName = os.listdir("log")

        for logName in logsName:
            with open("log/"+logName, "rb") as log:
                for line in log.readlines():
                    yield line.rstrip(b"\n").deBytes()

    
    def borrarLog(self, clienteId: uuid.UUID):    
        os.remove("log/"+str(clienteId))
        del self.logs[clienteId]


    def cerrar(self):
        for log in self.logs.values():
            log.close()