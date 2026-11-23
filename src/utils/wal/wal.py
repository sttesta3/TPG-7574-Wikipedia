from abc import ABC, abstractmethod
import os
import uuid
from collections.abc import Iterator
from protocolo.mensajesSistema import MensajeSistema
from enum import Enum

PATH_MSG = "logs/mensajes"
PATH_LOG = "logs/wal_log"
PATH_TMP = "logs/wal_log_tmp"
MENSAJES_PARA_CHECKPOINT = 100 

class Recipient(Enum):
    COLARESPUESTAS = 0
    EXCHANGETOPGLOBAL = 1

class LineaLog(Enum):
    REDOLOG = 0
    MSGSENT = 1
    RECVEOF = 2
    FINEOF = 3
    STARTCHECKPOINT = 4
    OKCHECKPOINT = 5
    ENDCHECKPOINT = 6


class Wal(ABC):
    def __init__(self) -> None:
        self.log_f = open(PATH_LOG,"ab")
        self.mensajes = open(PATH_MSG,"ab")
        self.cuenta_mensajes = 0

    def guardarEstado(self, bytes):
        self.log(LineaLog.STARTCHECKPOINT)
                
        self.log(LineaLog.ENDCHECKPOINT)


    @abstractmethod
    def recuperarEstado(self, function):
        function

    def guardarMensaje(self, mensaje: bytes, to: Recipient) -> None:
        self.mensajes.write(f"{self.cuenta_mensajes},{to},{mensaje}\n")
        self.log_f.write(f"{LineaLog.MSGSENT},{self.cuenta_mensajes}")
        self.cuenta_mensajes += 1

    def recuperarMensajes(self) -> Iterator[bytes]:
        return

        with open(PATH_LOGS, "rb",newline='\0') as log:
            for line in log.readlines():
                yield line.rstrip(b"\0").split(b"\1")[1].deBytes()

    
    def borrarLog(self):  
        os.remove(PATH_LOG)
        os.remove(PATH_MSG)


    def cerrar(self):
        self.mensajes.close()
        self.log_f.close()

    def log(self, linea: LineaLog, contenido: str | None ):
        write = f"{linea},{contenido}\n" if contenido else f"{linea}\n"
        self.log_f.write(write)
