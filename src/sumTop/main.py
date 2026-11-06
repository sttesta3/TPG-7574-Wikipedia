import os
import sys
import logging
import signal
import traceback
import threading
from clienteLock import ClienteLock
from middleware import MessageMiddlewareQueue, MessageMiddlewareExchange
from protocolo.mensajesSistema import recvMensajeSistema, FinMensajeSistema, PalabrasLoteMensajeSistema, PalabrasMensajeSistema

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


    def _procesarData(self, mensajes: PalabrasLoteMensajeSistema) -> None:
        clienteId = mensajes.clienteId
        if clienteId not in self.clientes:
            self.clientes[clienteId] = {}
            self.clientesLock[clienteId] = ClienteLock(TOTALTRANSFORMADORES)

        self.clientesLock[clienteId].nuevoMensaje()
        
        for mensaje in mensajes.mensajes:
            if mensaje.lenguaje not in self.clientes[clienteId]: 
                self.clientes[clienteId][mensaje.lenguaje] = {}

            for clave, valor in mensaje.palabras.items():
                self.clientes[clienteId][mensaje.lenguaje][clave] = self.clientes[clienteId][mensaje.lenguaje].get(clave, 0) + valor
            
        self.clientesLock[clienteId].nuevaRespuesta()


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
            logging.warning(e)
            logging.warning(traceback.format_exc())
            nack()


    def _manejarEof(self, bytes, ack, nack):
        try:
            mensaje = recvMensajeSistema(bytes)
            if self.clientesLock[mensaje.clienteId].llegadaEof():
                nodos = [{} for _ in range(TOTALTOPPARCIAL)]
                logging.info("1")
                # Afinidad palabras de cliente por nodo
                for lenguaje, palabras in self.clientes[mensaje.clienteId].items():
                    logging.debug("1.1")
                    for clave, valor in palabras.items():
                        logging.debug("1.1.1")
                        i = int.from_bytes(clave.encode("UTF-8")) % TOTALTOPPARCIAL
                        nodos[i][lenguaje] = nodos[i].get(lenguaje, {}) 
                        nodos[i][lenguaje][clave] = nodos[i][lenguaje].get(clave,valor)
                # Enviar palabras a cada nodo
                logging.debug("2")
                for i in range(TOTALTOPPARCIAL):
                    logging.debug("2.1")
                    for lenguaje, palabras in nodos[i].items():
                        logging.debug("2.1.1")
                        logging.debug(f"MANDO: {nodos[i]}")
                        mensaje = PalabrasLoteMensajeSistema(clienteId=mensaje.clienteId, mensajes=[PalabrasMensajeSistema(palabras=palabras, url="", lenguaje=lenguaje)])
                        self.excahangeTopParciales[i].send(mensaje.aBytes())
                    self.excahangeTopParciales[i].send(FinMensajeSistema(mensaje.clienteId).aBytes())

                del self.clientesLock[mensaje.clienteId]
                del self.clientes[mensaje.clienteId]
                
            ack()
        except Exception as e:
            logging.info("Guarda que sali en manejarEOF")
            logging.warning(traceback.format_exc())
            logging.warning(e)
            nack()
    
    
    def _controlarEof(self):
        self.exchangeSumTopEof.start_consuming(self._manejarEof)


    def iniciar(self):
        thread_eof = threading.Thread(target=self._controlarEof, daemon=True)
        thread_eof.start()
        self.colaSumTop.start_consuming(self.procesarMensaje)
        thread_eof.join()
        self._close_connections()



    def manejarSigterm(self) -> None:
        self.colaSumTop.remote_stop()
        self.exchangeSumTopEof.remote_stop()
        

    def _close_connections(self):
        self.colaSumTop.close()
        self.exchangeSumTopEof.close()
        self.exchangeSumTopEofSend.close()
        for i in range(TOTALTOPPARCIAL):
            self.excahangeTopParciales[i].close()



def main() -> int:
    logging.basicConfig(level=logging.INFO)
    sumTop = SumTop()
    signal.signal(signal.SIGTERM, lambda signum, frame: sumTop.manejarSigterm())
    sumTop.iniciar()
    return 0


if __name__ == "__main__":
    main()
