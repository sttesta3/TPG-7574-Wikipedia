import os
import sys
import uuid
import signal
import logging
import traceback
import threading
from contadorDistribuido import contadorDistribuido
from middleware import MessageMiddlewareQueue, MessageMiddlewareExchange
from protocolo.mensajesSistema import recvMensajeSistema, FinMensajeSistema, PalabrasLoteMensajeSistema, PalabrasMensajeSistema, MensajeSistema

MOMHOST = os.environ["MOMHOST"]
COLASUMTOP = os.environ["COLASUMTOP"]
EXCHANGESUMTOPEOF = os.environ["EXCHANGESUMTOPEOF"]
EXCHANGETOPPARCIAL = os.environ["EXCHANGETOPPARCIAL"]
TOTALTOPPARCIAL = int(os.environ["TOTALTOPPARCIAL"])

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


class SumTop:
    def __init__(self):
        self.colaSumTop = MessageMiddlewareQueue(MOMHOST, COLASUMTOP)
        self.excahangeTopParciales = []
        for i in range(TOTALTOPPARCIAL):
            self.excahangeTopParciales.append(MessageMiddlewareExchange(MOMHOST, EXCHANGETOPPARCIAL, [EXCHANGETOPPARCIAL+ "_"+str(i)]))

        self.contador = contadorDistribuido(MOMHOST, EXCHANGESUMTOPEOF, self._finalizarCliente, self.colaSumTop.remote_execution)

        self.clientes = {}

        self.wal = wal()


    def _recuperacion(self):
        for mensaje in self.wal.recuperarLogs():
            self._procesarData(mensaje, True)


    def _procesarData(self, mensajes: PalabrasLoteMensajeSistema, recuperacion: bool = False) -> None:
        if not recuperacion:
            self.wal.guardarMensaje(mensajes)

        clienteId = mensajes.clienteId
        if clienteId not in self.clientes:
            self.clientes[clienteId] = {}

        for mensaje in mensajes.mensajes:
            if mensaje.lenguaje not in self.clientes[clienteId]:
                self.clientes[clienteId][mensaje.lenguaje] = {}

            for clave, valor in mensaje.palabras.items():
                self.clientes[clienteId][mensaje.lenguaje][clave] = self.clientes[clienteId][mensaje.lenguaje].get(clave, 0) + valor


    def _finalizarCliente(self, clienteId, fin: FinMensajeSistema, originador: bool) -> None:
        palabrasCliente = self.clientes.pop(clienteId, {})
        self.wal.guardarMensaje(fin)

        nodos = [{} for _ in range(TOTALTOPPARCIAL)]
        for lenguaje, palabras in palabrasCliente.items():
            for clave, valor in palabras.items():
                i = int.from_bytes(clave.encode("UTF-8")) % TOTALTOPPARCIAL
                nodos[i][lenguaje] = nodos[i].get(lenguaje, {})
                nodos[i][lenguaje][clave] = nodos[i][lenguaje].get(clave,valor)

        for i in range(TOTALTOPPARCIAL):
            # TODO: como resolvemos esto
            for lenguaje, palabras in nodos[i].items():
                parcial = PalabrasLoteMensajeSistema(clienteId=clienteId, mensajes=[PalabrasMensajeSistema(palabras=palabras, url="", lenguaje=lenguaje)])
                self.excahangeTopParciales[i].send(parcial.aBytes())
            self.excahangeTopParciales[i].send(FinMensajeSistema(clienteId).aBytes())
        
        self.wal.borrarLog(clienteId)

        logging.info(f"Mando parciales y EOF de {clienteId}")


    def procesarMensaje(self, bytes, ack, nack):
        try:
            mensaje = recvMensajeSistema(bytes)
            if isinstance(mensaje, FinMensajeSistema):
                self.contador.eofRecibido(mensaje)
            elif self.contador.yaFinalizado(mensaje.clienteId):
                logging.info(f"Descarto lote {mensaje.secuencia} de {mensaje.clienteId}: cliente ya finalizado")
            else:
                self._procesarData(mensaje)
                self.contador.procesado(mensaje.clienteId, mensaje.secuencia)
            ack()
        except Exception as e:
            logging.warning(e)
            logging.warning(traceback.format_exc())
            nack()


    def iniciar(self):
        thread_contador = threading.Thread(target=self.contador.iniciar, daemon=True)
        thread_contador.start()
        self.colaSumTop.start_consuming(self.procesarMensaje)
        thread_contador.join()
        self._close_connections()


    def manejarSigterm(self) -> None:
        self.contador.detener()
        self.colaSumTop.remote_stop()


    def _close_connections(self):
        self.colaSumTop.close()
        for i in range(TOTALTOPPARCIAL):
            self.excahangeTopParciales[i].close()
        self.contador.cerrar()



def main() -> int:
    logging.basicConfig(level=logging.INFO)
    sumTop = SumTop()
    signal.signal(signal.SIGTERM, lambda signum, frame: sumTop.manejarSigterm())
    sumTop.iniciar()
    return 0


if __name__ == "__main__":
    main()
