import os
from mensajesGateway import Respuesta1Mensaje
from mensajesSistema import recvMensajeSistema, FinMensajeSistema, LoteDataMensajeSistema
from middleware import MessageMiddlewareQueue

MOMHOST = os.environ["MOMHOST"]
COLADATOS = os.environ["COLADATOS"]
COLARESPUESTAS = os.environ["COLARESPUESTAS"]
LENGUAJEINGLES = 1

class Clasificador:
    def __init__(self):
        self.colaDatos = MessageMiddlewareQueue(MOMHOST, COLADATOS)
        self.colaRespuestas = MessageMiddlewareQueue(MOMHOST, COLARESPUESTAS)


    def _procesarData(self, loteMensaje: LoteDataMensajeSistema) -> None:
        for mensaje in loteMensaje.lote:
            # Query 1:
            if mensaje.lenguaje == LENGUAJEINGLES and mensaje.fecha <= 2020:
                self.colaRespuestas.send(Respuesta1Mensaje(mensaje.url, mensaje.fecha).aBytes())
            else:
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
        self.colaDatos.start_consuming(self.procesarMensaje)

def main() -> int:
    clasificador = Clasificador()
    clasificador.iniciar()
    return 0


if __name__ == "__main__":
    main()