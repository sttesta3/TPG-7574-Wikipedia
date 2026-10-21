import os
from mensajesSistema import recvMensajeSistema, FinPromMensajeSistema, CantidadPalabraMensajeSistema, Respuesta5MensajeSistema
from middleware import MessageMiddlewareQueue, MessageMiddlewareExchange

MOMHOST = os.environ["MOMHOST"]
COLARESPUESTAS = os.environ["COLARESPUESTAS"]
EXCHANGECUENTAPROM = os.environ["EXCHANGECUENTAPROM"]
ID = os.environ["ID"]

class CuentaProm:
    def __init__(self):
        self.colaRespuestas = MessageMiddlewareQueue(MOMHOST, COLARESPUESTAS)
        self.exchangeProm = MessageMiddlewareExchange(MOMHOST, EXCHANGECUENTAPROM, [EXCHANGECUENTAPROM + "_" + ID])


    def _procesarData(self, mensaje: CantidadPalabraMensajeSistema) -> None:
        with open(str(mensaje.clienteId), "a", encoding="utf-8") as f:
            f.write(f"{mensaje.url},{mensaje.cantidad}")
            print(f"Guardo: {mensaje.url},{mensaje.cantidad}")


    def _procesarEOF(self, mensaje: FinPromMensajeSistema) -> None:

        with open(str(mensaje.clienteId), "r", encoding="utf-8") as f:
            for linea in f.readlines():
                cantidad, url = linea.strip().split(",", 1)
                if int(cantidad) > mensaje.promedio:
                    self.colaRespuestas.send(Respuesta5MensajeSistema(url, cantidad).aBytes())


    def procesarMensaje(self, bytes, ack, nack):
        mensaje = recvMensajeSistema(bytes)
        if isinstance(mensaje, FinPromMensajeSistema): # TODO: esta bien esto?
            self._procesarEOF(mensaje)
        else:
            self._procesarData(mensaje)
        ack()

    def iniciar(self):
        self.exchangeProm.start_consuming(self.procesarMensaje)

def main() -> int:
    cuentaProm = CuentaProm()
    cuentaProm.iniciar()
    return 0


if __name__ == "__main__":
    main()