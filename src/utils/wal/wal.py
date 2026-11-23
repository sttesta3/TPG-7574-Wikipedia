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

class LineaLog(Enum):
    RECVMSG = 0
    RABBITACKMSG = 1
    RABBITNACKMSG = 2
    MUTATESTATE = 3
    STOREMSG = 4 
    SENDMSG = 5
    STARTCHECKPOINT = 6
    ENDCHECKPOINT = 7


class Wal(ABC):
    def __init__(self) -> None:
        self.log = open(PATH_LOG,"ab")
        self.mensajes = open(PATH_MSG,"ab")
        self.cuenta_mensajes = 0

    @abstractmethod
    def guardarEstado(self):
        pass

    @abstractmethod
    def recuperarEstado(self):
        pass

    def guardarMensaje(self, mensaje: bytes, entrante:bool=True) -> None:
        self.mensajes.write(self.cuenta_mensajes + b"\1" + mensaje + b"\0")
        self.cuenta_mensajes += 1


    def recuperarMensajes(self) -> Iterator[bytes]:
        return

        with open(PATH_LOGS, "rb",newline='\0') as log:
            for line in log.readlines():
                yield line.rstrip(b"\0").deBytes()

    
    def borrarLog(self):  
        os.remove(PATH_LOG)
        os.remove(PATH_MSG)


    def cerrar(self):
        self.mensajes.close()
        self.log.close()

    def wal_log(self, linea: LineaLog):
        self.log.write(linea+'\0')