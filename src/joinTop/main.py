import os
import sys
import signal
import traceback
from middleware import MessageMiddlewareQueue, MessageMiddlewareExchange
from mensajesSistema import recvMensajeSistema, FinMensajeSistema, PalabrasMensajeSistema, Respuesta4MensajeSistema


MOMHOST = os.environ["MOMHOST"]
COLARESPUESTAS = os.environ["COLARESPUESTAS"]
EXCHANGETOPGLOBAL = os.environ["EXCHANGETOPGLOBAL"]
TOTALTOPPARCIAL = int(os.environ["TOTALTOPPARCIAL"])
ID = os.environ["ID"]


class JoinTop:
    def __init__(self):
        self.colaRespuestas = MessageMiddlewareQueue(MOMHOST, COLARESPUESTAS)
        self.exchangeTopGlobal = MessageMiddlewareExchange(MOMHOST, EXCHANGETOPGLOBAL, [EXCHANGETOPGLOBAL+"_"+ID])

        self.clientes = {}


    def _procesarData(self, mensaje: PalabrasMensajeSistema) -> None:
        if mensaje.clienteId not in self.clientes:
            self.clientes[mensaje.clienteId] = [0, {}]

        self.clientes[mensaje.clienteId][1] = self.clientes[mensaje.clienteId][1] | mensaje.palabras

    def _top20(self, palabras: dict[str, int]) -> dict[str, int]:
        top = sorted(palabras.items(), key=lambda item: item[1], reverse=True)
        return dict(top[:20])

    def _procesarEOF(self, mensaje: FinMensajeSistema) -> None:
        self.clientes[mensaje.clienteId][0] += 1

        if self.clientes[mensaje.clienteId][0] == TOTALTOPPARCIAL:
            self.colaRespuestas.send(Respuesta4MensajeSistema(mensaje.clienteId, self._top20(self.clientes[mensaje.clienteId][1])).aBytes())
            self.colaRespuestas.send(mensaje.aBytes())
            del self.clientes[mensaje.clienteId]


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


    def iniciar(self):
        self.exchangeTopGlobal.start_consuming(self.procesarMensaje)


    def manejarSigterm(self) -> None:
        self.colaRespuestas.close()
        self.exchangeTopGlobal.close()
        sys.exit(0)


def main() -> int:
    joinTop = JoinTop()
    signal.signal(signal.SIGTERM, lambda signum, frame: joinTop.manejarSigterm())
    joinTop.iniciar()
    return 0


if __name__ == "__main__":
    main()