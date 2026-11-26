import os
import uuid
import signal
import logging
import traceback
import threading
from latido import Latido
from wal import Wal, LineaLog
from contadorEof import contadorEof
from middleware import MessageMiddlewareQueue
from protocolo.mensajesSistema import recvMensajeSistema, FinMensajeSistema, PalabrasLoteMensajeSistema, Respuesta4MensajeSistema, ETAPA_JOIN, origenGateway, ClienteMuertoMensajeSistema


MOMHOST = os.environ["MOMHOST"]
COLARESPUESTAS = os.environ["COLARESPUESTAS"]
COLATOPGLOBAL = os.environ["COLATOPGLOBAL"]
TOTALTOPPARCIAL = int(os.environ["TOTALTOPPARCIAL"])
ID = os.environ["ID"]


class WalJoinTop(Wal):
    def __init__(self):
        super().__init__()


    def guardarEstado(self, estado: dict[uuid.UUID, list[int, dict[str, int]]]):
        self.wal_log(LineaLog.STARTCHECKPOINT)
        
        tmp = open("tmp", "a")

        for cliente, EofYPalabras in estado.items():
            tmp.write(str(cliente) + "|" + EofYPalabras[0] + ":")
            for palabra, cantidad in EofYPalabras[1].items():
                tmp.write("|" +palabra + ":" + cantidad)
            tmp.write("\n")
        
        tmp.flush()
        tmp.close()
        os.replace("tmp", "checkpoint")

        self.wal_log(LineaLog.ENDCHECKPOINT)


    def recuperarEstado(self) -> dict[uuid.UUID, list[int, dict[str, int]]]:
        
        rta = {}
        
        with open("estado", "r") as f:
            for line in f.readlines():

                splited  = line.split(":|")
                clienteId = uuid.UUID(splited[0].split("|")[0])
                
                tmp = {}
                for x in splited[1].split("|"):
                    palabra, cantidad = x.split(":", 1)
                    tmp[palabra] = cantidad

                rta[clienteId] = [splited[0].split("|")[1], tmp]
                        
        return rta


class JoinTop:
    def __init__(self):
        self.colaRespuestas = MessageMiddlewareQueue(MOMHOST, COLARESPUESTAS)
        self.colaTopGlobal = MessageMiddlewareQueue(MOMHOST, COLATOPGLOBAL + "_" + ID)

        self.clientes = {}
        self.contador = contadorEof(TOTALTOPPARCIAL)
        self.wal = WalJoinTop()


    def _procesarData(self, mensajes: PalabrasLoteMensajeSistema) -> None:
        clienteId = mensajes.clienteId
        if clienteId not in self.clientes:
            self.clientes[clienteId] = {}

        for mensaje in mensajes.mensajes:
            logging.info(f"[join] Recibi {clienteId} top parcial {mensaje.palabras}")
            self.clientes[clienteId] = self.clientes[clienteId] | mensaje.palabras

    def _top20(self, palabras: dict[str, int]) -> dict[str, int]:
        top = sorted(palabras.items(), key=lambda item: item[1], reverse=True)
        return dict(top[:20])

    def _procesarEOF(self, mensaje: FinMensajeSistema) -> None:
        logging.info(f"[join] Recibi {mensaje.clienteId} EOF de {mensaje.origen}")
        if self.contador.eofRecibido(mensaje.clienteId, mensaje.origen):
            palabras = self.clientes.pop(mensaje.clienteId, {})
            idRespuesta = (ETAPA_JOIN, int(ID), 0, 0)
            self.colaRespuestas.send(Respuesta4MensajeSistema(mensaje.clienteId, self._top20(palabras), idRespuesta).aBytes())
            self.colaRespuestas.send(FinMensajeSistema(mensaje.clienteId, origen=origenGateway(ETAPA_JOIN, int(ID))).aBytes())
            self.contador.finalizar(mensaje.clienteId)
            self.wal.borrarLog(mensaje.clienteId)
            del self.clientes[mensaje.clienteId]



    def procesarMensaje(self, bytes, ack, nack):
        try:
            mensaje = recvMensajeSistema(bytes)
            if isinstance(mensaje, FinMensajeSistema):
                self._procesarEOF(mensaje)
            elif self.contador.yaFinalizado(mensaje.clienteId):
                logging.info(f"Descarto parcial de {mensaje.clienteId}: cliente ya finalizado")
            elif self.contador.yaProcesado(mensaje.clienteId, mensaje.secuencia):
                logging.info(f"Descarto parcial {mensaje.secuencia} de {mensaje.clienteId}: duplicado")
            elif isinstance(mensaje, ClienteMuertoMensajeSistema):
                del self.clientes[mensaje.clientId]
            else:
                self._procesarData(mensaje)
                self.contador.procesado(mensaje.clienteId, mensaje.secuencia)
            ack()
        except Exception as e:
            logging.info(e)
            logging.info(traceback.format_exc())
            nack()


    def _recuperarLog(self):
        for log in self.wal.recuperarLogs():
            if isinstance(log, FinMensajeSistema):
                self._procesarEOF(log)
            else:
                self._procesarData(log)


    def iniciar(self):
        latido = Latido(self.exchangeTopGlobal.connection)
        thread_latido = threading.Thread(target=latido.start, daemon=True)
        thread_latido.start()

        self._recuperarLog()
        self.colaTopGlobal.start_consuming(self.procesarMensaje)
        self._close_connections()


    def manejarSigterm(self) -> None:
        self.colaTopGlobal.remote_stop()


    def _close_connections(self):
        self.colaRespuestas.close()
        self.colaTopGlobal.close()


def main() -> int:
    logging.basicConfig(level=logging.INFO)
    joinTop = JoinTop()
    signal.signal(signal.SIGTERM, lambda signum, frame: joinTop.manejarSigterm())
    joinTop.iniciar()
    return 0


if __name__ == "__main__":
    main()
