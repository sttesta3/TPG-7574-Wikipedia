from abc import ABC, abstractmethod
import os
import uuid
from collections.abc import Iterator
from protocolo.mensajesSistema import MensajeSistema
from enum import Enum

PATH_LOGS = "logs/mensajes"
 
class LineaLog(Enum):
    RECVMSG = 0
    RABBITACKMSG = 1
    RABBITNACKMSG = 2
    MUTATESTATE = 3
    STOREMSG = 4 
    SENDMSG = 5


class Wal(ABC):
    def __init__(self) -> None:
        self.log_mensajes = {}

    @abstractmethod
    def guardarEstado(self):
        pass

    @abstractmethod
    def recuperarEstado(self):
        pass

    def guardarMensaje(self, mensaje: bytes, entrante:bool=True) -> None:
        if not self.log_mensajes:
            self.log_mensajes = open(PATH_LOGS,"ab")
        self.log_mensajes.write(mensaje + b"\0")


    def recuperarLogs(self) -> Iterator[bytes]:
        return

        with open(PATH_LOGS, "rb",newline='\0') as log:
            for line in log.readlines():
                yield line.rstrip(b"\0").deBytes()

    
    def borrarLog(self):  
        os.remove(PATH_LOGS)


    def cerrar(self):
        self.log_mensajes.close()
