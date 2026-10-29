import os
import sys
import signal
import threading
from mensajesSistema import recvMensajeSistema, FinMensajeSistema, TransformadorMensajeSistema, PalabrasMensajeSistema, CantidadPalabraMensajeSistema
from middleware import MessageMiddlewareQueue, MessageMiddlewareExchange

import traceback

MOMHOST = os.environ["MOMHOST"]
COLASUMTOP = os.environ["COLASUMTOP"]
EXCHANGESUMTOPEOF = os.environ["EXCHANGESUMTOPEOF"]
EXCHANGETOPPARCIAL = os.environ["EXCHANGETOPPARCIAL"]
TOTALTOPPARCIAL = int(os.environ["TOTALTOPPARCIAL"])


class SumTop:
    def __init__(self):
        self.colaSumTop = MessageMiddlewareQueue(MOMHOST, COLASUMTOP)
        self.exchangeSumTopEofSend = MessageMiddlewareExchange(MOMHOST, EXCHANGESUMTOPEOF, [EXCHANGESUMTOPEOF])
        self.exchangeSumTopEof = MessageMiddlewareExchange(MOMHOST, EXCHANGESUMTOPEOF, [EXCHANGESUMTOPEOF])
        self.excahangeTopParciales = []
        for i in range(TOTALTOPPARCIAL):
            self.excahangeTopParciales.append(MessageMiddlewareExchange(MOMHOST, EXCHANGETOPPARCIAL, [EXCHANGETOPPARCIAL+ "_"+str(i)]))

        self.clientes = {}
        self.lock = threading.Lock()


    def _procesarData(self, mensaje: PalabrasMensajeSistema) -> None:
        with self.lock:
            if mensaje.clienteId not in self.clientes:
                self.clientes[mensaje.clienteId] = {}
            if mensaje.language not in self.clientes[mensaje.clienteId]: 
                self.clientes[mensaje.clienteId][mensaje.language] = {}

            for clave, valor in mensaje.palabras.items():
                self.clientes[mensaje.clienteId][mensaje.language][clave] = self.clientes[mensaje.clienteId][mensaje.language].get(clave, 0) + valor


    def _procesarEOF(self, mensaje: FinMensajeSistema) -> None:
        print("LLEGO EOF")
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
            print(e)
            print(traceback.format_exc())
            nack()


    def _manejarEof(self, bytes, ack, nack):
        try:
            mensaje = recvMensajeSistema(bytes)
            with self.lock:
                nodos = [{} for _ in range(TOTALTOPPARCIAL)]
                for lenguaje, palabras in self.clientes[mensaje.clienteId].items():
                    for clave, valor in palabras:
                        i = int.from_bytes(clave.encode("UTF-8")) % TOTALTOPPARCIAL
                        nodos[i][lenguaje][clave] = valor

                for i in range(TOTALTOPPARCIAL):
                    for lenguaje, palabras in nodos[i]:
                        print(f"MANDO: {nodos[i]}")
                        mensaje = PalabrasMensajeSistema(palabras=palabras, clienteId=mensaje.clienteId, url="", lenguaje=lenguaje)
                        self.excahangeTopParciales[i].send(mensaje.aBytes())
                    self.excahangeTopParciales[i].send(FinMensajeSistema(mensaje.clienteId).aBytes())
                
            ack()
        except Exception as e:
            print(e)
            nack()
    
    
    def _controlarEof(self):
        self.exchangeSumTopEof.start_consuming(self._manejarEof)


    def iniciar(self):
        threading.Thread(target=self._controlarEof, daemon=True).start()
        self.colaSumTop.start_consuming(self.procesarMensaje)


    def manejarSigterm(self) -> None:
        pass


def main() -> int:
    sumTop = SumTop()
    signal.signal(signal.SIGTERM, lambda signum, frame: sumTop.manejarSigterm())
    sumTop.iniciar()
    return 0


if __name__ == "__main__":
    main()