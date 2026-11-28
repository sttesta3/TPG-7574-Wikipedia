import os
import uuid
from enum import Enum
from abc import ABC
from collections.abc import Iterator
from protocolo.mensajesSistema import MensajeSistema
import json 

PATH_MSG = "/states/mensajes"
PATH_LOG = "/states/wal_log"
PATH_EST = "/states/estado"
PATH_CTD = "/states/contador"
PATH_EST_TMP = f"{PATH_EST}_TMP"
PATH_CTD_TMP = f"{PATH_CTD}_TMP"
MENSAJES_PARA_CHECKPOINT = 10

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
        self.log_f = open(PATH_LOG,"a")
        self.mensajes = open(PATH_MSG,"ab")
        self.cuenta_mensajes = 0


    def guardarEstado(self, state: dict, state_contador: list):
        self.log(LineaLog.STARTCHECKPOINT, None)

        self._dump_state(file=PATH_EST_TMP, content=state)
        self._dump_state(file=PATH_CTD_TMP, content=state_contador)

        self.estadoTemporalAPermanente()
        self.truncarRedoLog()

        self.log(LineaLog.ENDCHECKPOINT, None)
        
        self.cuenta_mensajes = 0


    def _dump_state(self,file: str, content: dict | list) :
        with open(file,"w") as f:
            f.write(json.dumps(self._normalize_keys(content), ensure_ascii=False, separators=(",", ":")))
            f.flush()
            os.fsync(f.fileno())


    def _normalize_keys(self, content):
        if isinstance(content, dict):
            return {str(k) if isinstance(k, uuid.UUID) else k: self._normalize_keys(v) for k, v in content.items()}
        elif isinstance(content, list) or isinstance(content, set):
            return [self._normalize_keys(item) for item in content]
        elif isinstance(content, uuid.UUID):
            return str(content)
        elif not isinstance(content, str) and not isinstance(content, int) and not isinstance(content, set):
            return content.serialize()
        return content


    def recuperarEstado(self) -> list[dict,list]:
        try:
            with open(PATH_EST,"r") as f:
                non_normalized_state = json.loads(f.read())

                state = {
                    uuid.UUID(cliente_id): {
                        int(lenguaje): palabras
                        for lenguaje, palabras in lenguajes.items()
                    }
                    for cliente_id, lenguajes in non_normalized_state.items()
                }
            with open(PATH_CTD,"r") as f:
                contador_state = json.loads(f.read())
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


    def guardarMensaje(self, mensaje: bytes) -> None:
        self.mensajes.write(len(mensaje).to_bytes(4, byteorder="big"))
        self.mensajes.write(mensaje)

        self.mensajes.flush()
        os.fsync(self.mensajes.fileno())

        self.cuenta_mensajes += 1


    def recuperarMensajes(self) -> Iterator[bytes]:
        with open(PATH_MSG, "rb") as log:
            while True:
                header = log.read(4)

                if not header:
                    break
                
                if len(header) != 4:
                    raise IOError("Header incompleto en WAL")

                largo = int.from_bytes(header, byteorder="big")

                if largo <= 0:
                    raise IOError("Longitud inválida en WAL")

                msg = log.read(largo)

                if len(msg) != largo:
                    raise IOError("Mensaje incompleto en WAL")

                yield msg
    

    def borrarLog(self):  
        os.remove(PATH_LOG)
        os.remove(PATH_MSG)


    def cerrar(self):
        self.mensajes.close()
        self.log_f.close()


    def log(self, linea: LineaLog, contenido: str | None ):
        write_line = f"{linea},{contenido}\n" if contenido else f"{linea}\n"
        write_bytes = write_line
        self.log_f.write(write_bytes)


    def tiempoDeCheckpoint(self) -> bool:
        #print(f"Tiempo de checkpoint: {self.cuenta_mensajes > MENSAJES_PARA_CHECKPOINT}")
        return self.cuenta_mensajes >= MENSAJES_PARA_CHECKPOINT
