import os
import uuid
from enum import Enum
from abc import ABC, abstractmethod
from collections.abc import Iterator
from protocolo.mensajesSistema import MensajeSistema

# TODO: poner volumen de logs/ en cada nodo 
PATH_MSG = "mensajes"
PATH_LOG = "wal_log"
PATH_EST = "estado"
PATH_EST_TMP = f"{PATH_EST}_TMP"
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
        with open(PATH_EST_TMP,"ab") as f:
            f.write(bytes)

    def recuperarEstado(self):
        with open(PATH_EST,"ab") as f:
            f.write(bytes)

    def estadoTemporalAPermanente(self):
        os.rename(PATH_EST_TMP,PATH_EST)

    def truncarRedoLog(self):
        with open(PATH_MSG,"w") as f:
            f.truncate(0)
        with open(PATH_LOG,"w") as f:
            f.truncate(0)

    def guardarMensaje(self, mensaje: bytes, to: Recipient) -> None:
        self.mensajes.write(f"{self.cuenta_mensajes},{to},{mensaje}\n")
        self.log_f.write(f"{LineaLog.MSGSENT},{self.cuenta_mensajes}")
        self.cuenta_mensajes += 1

    def recuperarMensajes(self) -> Iterator[bytes]:
        return

        with open(PATH_LOGS, "rb") as log:
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


    def tiempoDeCheckpoint(self) -> bool:
        return self.cuenta_mensajes == MENSAJES_PARA_CHECKPOINT