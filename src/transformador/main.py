import os
from mensajesSistema import recvMensajeSistema, FinMensajeSistema, TransformadorMensajeSistema
from middleware import MessageMiddlewareQueue

MOMHOST = os.environ["MOMHOST"]
COLATRANSFORMADOR = os.environ["COLATRANSFORMADOR"]

LENGUAJEINGLES = 1

class Transformador:
    def __init__(self):
        self.colaTransformador = MessageMiddlewareQueue(MOMHOST, COLATRANSFORMADOR)


    def _procesarData(self, loteMensaje: TransformadorMensajeSistema) -> None:
        pass
            

    def _procesarEOF(self, mensaje: FinMensajeSistema) -> None:
        pass


    def procesarMensaje(self, bytes, ack, nack):
        mensaje = recvMensajeSistema(bytes)
        if isinstance(mensaje, FinMensajeSistema): # TODO: esta bien esto?
            self._procesarEOF(mensaje)
        else:
            self._procesarData(mensaje)
        ack()

    def iniciar(self):
        self.colaTransformador.start_consuming(self.procesarMensaje)

def main() -> int:
    transformador = Transformador()
    transformador.iniciar()
    return 0


if __name__ == "__main__":
    main()