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

            for clave, valor in mensaje.palabras.items():
                self.clientes[mensaje.clienteId][clave] = self.clientes[mensaje.clienteId].get(clave, 0) + valor


    def _procesarEOF(self, mensaje: FinMensajeSistema) -> None:
        print(f"teetas {self.clientes[mensaje.clienteId]} ")
        self.exchangeSumTopEofSend.send(mensaje.aBytes())


    def procesarMensaje(self, bytes, ack, nack):
        try:
            mensaje = recvMensajeSistema(bytes)
            if isinstance(mensaje, FinMensajeSistema): # TODO: esta bien esto?
                print(f"recivo EOF de {mensaje.clienteId}")
                self._procesarEOF(mensaje)
            else:
                self._procesarData(mensaje)
            ack()
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            nack()


    def _controlarEof(self):

        def manejareEof(bytes, ack, nack):
            try:
                mensaje = recvMensajeSistema(bytes)

                with self.lock:
                    print(f" {self.clientes[mensaje.clienteId]} ")
                
                ack()
            except Exception as e:
                print(e)
                nack()

        self.exchangeSumTopEof.start_consuming(manejareEof)


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