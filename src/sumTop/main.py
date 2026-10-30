import os
import sys
import logging
import signal
import traceback
import threading
from clienteLock import ClienteLock
from middleware import MessageMiddlewareQueue, MessageMiddlewareExchange
from protocolo.mensajesSistema import recvMensajeSistema, FinMensajeSistema, PalabrasMensajeSistema

MOMHOST = os.environ["MOMHOST"]
COLASUMTOP = os.environ["COLASUMTOP"]
EXCHANGESUMTOPEOF = os.environ["EXCHANGESUMTOPEOF"]
EXCHANGETOPPARCIAL = os.environ["EXCHANGETOPPARCIAL"]
TOTALTOPPARCIAL = int(os.environ["TOTALTOPPARCIAL"])
TOTALTRANSFORMADORES = int(os.environ["TOTALTRANSFORMADORES"])


class SumTop:
    def __init__(self):
        self.colaSumTop = MessageMiddlewareQueue(MOMHOST, COLASUMTOP)
        self.exchangeSumTopEofSend = MessageMiddlewareExchange(MOMHOST, EXCHANGESUMTOPEOF, [EXCHANGESUMTOPEOF])
        self.exchangeSumTopEof = MessageMiddlewareExchange(MOMHOST, EXCHANGESUMTOPEOF, [EXCHANGESUMTOPEOF])
        self.excahangeTopParciales = []
        for i in range(TOTALTOPPARCIAL):
            self.excahangeTopParciales.append(MessageMiddlewareExchange(MOMHOST, EXCHANGETOPPARCIAL, [EXCHANGETOPPARCIAL+ "_"+str(i)]))

        self.clientes = {}
        self.clientesLock = {}


    def _procesarData(self, mensaje: PalabrasMensajeSistema) -> None:
        if mensaje.clienteId not in self.clientes:
            self.clientes[mensaje.clienteId] = {}
            self.clientesLock[mensaje.clienteId] = ClienteLock(TOTALTRANSFORMADORES)
        if mensaje.language not in self.clientes[mensaje.clienteId]: 
            self.clientes[mensaje.clienteId][mensaje.language] = {}

        self.clientesLock[mensaje.clienteId].nuevoMensaje()
        for clave, valor in mensaje.palabras.items():
            self.clientes[mensaje.clienteId][mensaje.language][clave] = self.clientes[mensaje.clienteId][mensaje.language].get(clave, 0) + valor
        self.clientesLock[mensaje.clienteId].nuevaRespuesta()

    def _procesarEOF(self, mensaje: FinMensajeSistema) -> None:
        self.exchangeSumTopEofSend.send(mensaje.aBytes())


    def procesarMensaje(self, bytes, ack, nack):
        try:
            mensaje = recvMensajeSistema(bytes)
            if isinstance(mensaje, FinMensajeSistema): # TODO: esta bien esto?
                self._procesarEOF(mensaje)
            else:
                self._procesarData(mensaje)
            ack()
        except Exception as e:
            logging.info(e)
            logging.info(traceback.format_exc())
            nack()


    def _manejarEof(self, bytes, ack, nack):
        try:
            mensaje = recvMensajeSistema(bytes)
            if self.clientesLock[mensaje.clienteId].llegadaEof():
                nodos = [{} for _ in range(TOTALTOPPARCIAL)]
                for lenguaje, palabras in self.clientes[mensaje.clienteId].items():
                    for clave, valor in palabras:
                        i = int.from_bytes(clave.encode("UTF-8")) % TOTALTOPPARCIAL
                        nodos[i][lenguaje][clave] = valor

                for i in range(TOTALTOPPARCIAL):
                    for lenguaje, palabras in nodos[i]:
                        logging.info(f"MANDO: {nodos[i]}")
                        mensaje = PalabrasMensajeSistema(palabras=palabras, clienteId=mensaje.clienteId, url="", lenguaje=lenguaje)
                        self.excahangeTopParciales[i].send(mensaje.aBytes())
                    self.excahangeTopParciales[i].send(FinMensajeSistema(mensaje.clienteId).aBytes())

                del self.clientesLock[mensaje.clienteId]
                del self.clientes[mensaje.clienteId]
                
            ack()
        except Exception as e:
            logging.info(e)
            nack()
    
    
    def _controlarEof(self):
        self.exchangeSumTopEof.start_consuming(self._manejarEof)


    def iniciar(self):
        threading.Thread(target=self._controlarEof, daemon=True).start()
        self.colaSumTop.start_consuming(self.procesarMensaje)


    def manejarSigterm(self) -> None:
        self.colaSumTop.close()
        self.exchangeSumTopEof.close()
        self.exchangeSumTopEofSend.close()
        for i in range(TOTALTOPPARCIAL):
            self.excahangeTopParciales[i].close()
        sys.exit(0)


def main() -> int:
    sumTop = SumTop()
    signal.signal(signal.SIGTERM, lambda signum, frame: sumTop.manejarSigterm())
    sumTop.iniciar()
    return 0


if __name__ == "__main__":
    main()
