from protocolo.mensajesSistema import MensajeSistema
from collections.abc import Iterator

class wal():
    def __init__(self) -> None:
        self.logs = {}


    def guardarMensaje(self, mensaje: MensajeSistema) -> None:
        if mensaje.clienteId not in self.logs:
            self.logs[mensaje.clienteId] = open("log/"+str(mensaje.clienteId), "ab")

        self.logs[mensaje.clienteId].write(mensaje.aBytes() + b"\n")


    def recuperarLogs(self) -> Iterator[bytes]:
        logsName = os.listdir("/log")

        for logName in logsName:
            with open("/log/"+logName, "rb") as log:
                for line in log.readlines():
                    yield line.rstrip(b"\n").deBytes() # TODO: hacer esto bien

    
    def borrarLog(self, clienteId: uuid.UUID):    
        os.remove("log/"+str(clienteId))
        del self.logs[clienteId]


    def cerrar(self):
        for log in self.logs.values():
            log.close()