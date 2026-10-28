import os
import sys
import signal
from middleware import MessageMiddlewareQueue, MessageMiddlewareExchange
from mensajesSistema import recvMensajeSistema, FinPromMensajeSistema, CantidadPalabraMensajeSistema, Respuesta5MensajeSistema, FinMensajeSistema

MOMHOST = os.environ["MOMHOST"]
COLARESPUESTAS = os.environ["COLARESPUESTAS"]
EXCHANGECUENTAPROM = os.environ["EXCHANGECUENTAPROM"]
ID = os.environ["ID"]


class CuentaProm:
    def __init__(self):
        self.clientes = {}
        self.colaRespuestas = MessageMiddlewareQueue(MOMHOST, COLARESPUESTAS)
        self.exchangeProm = MessageMiddlewareExchange(MOMHOST, EXCHANGECUENTAPROM, [EXCHANGECUENTAPROM + "_" + ID])


    def _procesarData(self, mensaje: CantidadPalabraMensajeSistema) -> None:
        clientId = str(mensaje.clienteId)
        self.clientes[clientId] = 0
        with open(clientId, "a", encoding="utf-8") as f:
            f.write(f"{mensaje.url};;;;;{mensaje.cantidad}\n")


    def _procesarEOF(self, mensaje: FinPromMensajeSistema) -> None:
        with open(str(mensaje.clienteId), "r", encoding="utf-8") as f:
            for linea in f.readlines():
                url, cantidad = linea.strip().split(";;;;;", 1)
                if int(cantidad) > mensaje.promedio:
                    self.colaRespuestas.send(Respuesta5MensajeSistema(mensaje.clienteId,  url, int(cantidad)).aBytes())
        self.colaRespuestas.send(FinMensajeSistema(mensaje.clienteId).aBytes())
        
        os.remove(str(mensaje.clienteId))
        del self.clientes[str(mensaje.clienteId)]
        

    def procesarMensaje(self, bytes, ack, nack):
        try:
            mensaje = recvMensajeSistema(bytes)
            if isinstance(mensaje, FinPromMensajeSistema): # TODO: esta bien esto?
                self._procesarEOF(mensaje)
            else:
                self._procesarData(mensaje)
            ack()
        except Exception as e:
            print(e)
            nack()


    def iniciar(self):
        self.exchangeProm.start_consuming(self.procesarMensaje)


    def manejarSigterm(self) -> None:
        self.exchangeProm.close()
        self.colaRespuestas.close()
        sys.exit(0)


def main() -> int:
    cuentaProm = CuentaProm()
    signal.signal(signal.SIGTERM, lambda signum, frame: cuentaProm.manejarSigterm())
    cuentaProm.iniciar()
    return 0


if __name__ == "__main__":
    main()