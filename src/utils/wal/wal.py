import os
import uuid
from enum import Enum
from abc import ABC
from collections.abc import Iterator
from protocolo.mensajesSistema import MensajeSistema
import json 

# TODO: poner volumen de logs/ en cada nodo 
PATH_MSG = "/states/mensajes"
PATH_LOG = "/states/wal_log"
PATH_EST = "/states/estado"
PATH_CTD = "/states/contador"
PATH_EST_TMP = f"{PATH_EST}_TMP"
PATH_CTD_TMP = f"{PATH_CTD}_TMP"
MENSAJES_PARA_CHECKPOINT = 1

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

    def guardarEstado(self, state: dict, state_contador: list):
        self.log(LineaLog.STARTCHECKPOINT, None)

        self._dump_state(file=PATH_EST_TMP, content=state)
        self._dump_state(file=PATH_CTD_TMP, content=state_contador)

        self.log(LineaLog.ENDCHECKPOINT, None)
        self.estadoTemporalAPermanente()
        self.truncarRedoLog()
        
        self.cuenta_mensajes = 0

    def _dump_state(self,file: str, content: dict | list) :
        with open(file,"wb") as f:
            f.write(json.dumps(content, ensure_ascii=False, separators=(",", ":")).encode("utf-8"))
            f.flush()
            os.fsync(f.fileno())

    def recuperarEstado(self) -> list[dict,list]:
        try:
            with open(PATH_EST,"rb") as f:
                state = json.loads(f.read().decode("utf-8"))
            with open(PATH_CTD,"rb") as f:
                contador_state = json.loads(f.read().decode("utf-8"))
            return [state, contador_state]
        except Exception: # TODO: Super generico 
            return [{}, []]

    def estadoTemporalAPermanente(self):
        os.rename(PATH_EST_TMP,PATH_EST)
        os.rename(PATH_CTD_TMP,PATH_CTD)

    def truncarRedoLog(self):
        with open(PATH_MSG,"w") as f:
            f.truncate(0)
        with open(PATH_LOG,"w") as f:
            f.truncate(0)

    def guardarMensaje(self, mensaje: bytes, to: Recipient) -> None:
        self.mensajes.write(f"{self.cuenta_mensajes},{to},{mensaje}\n".encode("UTF-8"))
        self.log_f.write(f"{LineaLog.MSGSENT},{self.cuenta_mensajes}\n".encode("UTF-8"))
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
        write_line = f"{linea},{contenido}\n" if contenido else f"{linea}\n"
        write_bytes = write_line.encode("utf-8")
        self.log_f.write(write_bytes)


    def tiempoDeCheckpoint(self) -> bool:
        print(f"Tiempo de checkpoint: {self.cuenta_mensajes > MENSAJES_PARA_CHECKPOINT}")
        return self.cuenta_mensajes >= MENSAJES_PARA_CHECKPOINT
