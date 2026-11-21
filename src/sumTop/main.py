import os
import signal
import logging
import traceback
import threading
from wal import Wal
from contadorDistribuido import contadorDistribuido
from middleware import MessageMiddlewareQueue, MessageMiddlewareExchange
from protocolo.mensajesSistema import recvMensajeSistema, FinMensajeSistema, PalabrasLoteMensajeSistema, PalabrasMensajeSistema

MOMHOST = os.environ["MOMHOST"]
COLASUMTOP = os.environ["COLASUMTOP"]
EXCHANGESUMTOPEOF = os.environ["EXCHANGESUMTOPEOF"]
EXCHANGETOPPARCIAL = os.environ["EXCHANGETOPPARCIAL"]
TOTALTOPPARCIAL = int(os.environ["TOTALTOPPARCIAL"])


class SumTop:
    def __init__(self):
        self.colaSumTop = MessageMiddlewareQueue(MOMHOST, COLASUMTOP)
        self.excahangeTopParciales = []
        for i in range(TOTALTOPPARCIAL):
            self.excahangeTopParciales.append(MessageMiddlewareExchange(MOMHOST, EXCHANGETOPPARCIAL, [EXCHANGETOPPARCIAL+ "_"+str(i)]))

        self.contador = contadorDistribuido(MOMHOST, EXCHANGESUMTOPEOF, self._finalizarCliente, self.colaSumTop.remote_execution)

        self.clientes = {}
        self.wal = Wal()


    def _procesarData(self, mensajes: PalabrasLoteMensajeSistema) -> None:
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

        nodos = [{} for _ in range(TOTALTOPPARCIAL)]
        for lenguaje, palabras in palabrasCliente.items():
            for clave, valor in palabras.items():
                i = int.from_bytes(clave.encode("UTF-8")) % TOTALTOPPARCIAL
                nodos[i][lenguaje] = nodos[i].get(lenguaje, {})
                nodos[i][lenguaje][clave] = nodos[i][lenguaje].get(clave,valor)

        for i in range(TOTALTOPPARCIAL):
            for lenguaje, palabras in nodos[i].items():
                parcial = PalabrasLoteMensajeSistema(clienteId=clienteId, mensajes=[PalabrasMensajeSistema(palabras=palabras, url="", lenguaje=lenguaje)])
                self.excahangeTopParciales[i].send(parcial.aBytes())
            self.excahangeTopParciales[i].send(FinMensajeSistema(clienteId).aBytes())

        self.wal.borrarLog(clienteId)
        logging.debug(f"Mando parciales y EOF de {clienteId}")


    def procesarMensaje(self, bytes, ack, nack):
        try:
            mensaje = recvMensajeSistema(bytes)
            self.wal.guardarMensaje(bytes, mensaje.clienteId)
            if isinstance(mensaje, FinMensajeSistema):
                self.contador.eofRecibido(mensaje)
            elif self.contador.yaFinalizado(mensaje.clienteId):
                logging.debug(f"Descarto lote {mensaje.secuencia} de {mensaje.clienteId}: cliente ya finalizado")
            else:
                self.contador.procesado(mensaje.clienteId, mensaje.secuencia)
                self._procesarData(mensaje)
            ack()
        except Exception as e:
            logging.warning(e)
            logging.warning(traceback.format_exc())
            nack()


    def _recuperarLog(self):
        for log in self.wal.recuperarLogs():
            if isinstance(log, FinMensajeSistema):
                self.contador.eofRecibido(log)
            elif self.contador.yaFinalizado(log.clienteId):
                logging.debug(f"Descarto lote {log.secuencia} de {log.clienteId}: cliente ya finalizado")
            else:
                self.contador.procesado(log.clienteId, log.secuencia)
                self._procesarData(log)


    def iniciar(self):
        self._recuperarLog()
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
