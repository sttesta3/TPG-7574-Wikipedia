import os
from mensajesSistema import recvMensajeSistema, FinMensajeSistema, LoteDataMensajeSistema, ImgMensajeSistema, Respuesta1MensajeSistema, TransformadorMensajeSistema
from middleware import MessageMiddlewareQueue

MOMHOST = os.environ["MOMHOST"]
COLADATOS = os.environ["COLADATOS"]
COLARESPUESTAS = os.environ["COLARESPUESTAS"]
COLAIMGDOWLOADER = os.environ["COLAIMGDOWLOADER"]
COLATRANSFORMADOR = os.environ["COLATRANSFORMADOR"]

LENGUAJEINGLES = 1

class Clasificador:
    def __init__(self):
        self.colaDatos = MessageMiddlewareQueue(MOMHOST, COLADATOS)
        self.colaRespuestas = MessageMiddlewareQueue(MOMHOST, COLARESPUESTAS)
        self.colaImgDowloader = MessageMiddlewareQueue(MOMHOST, COLAIMGDOWLOADER)
        self.colaTransformador = MessageMiddlewareQueue(MOMHOST, COLATRANSFORMADOR)


    def _procesarData(self, loteMensaje: LoteDataMensajeSistema) -> None:
        for mensaje in loteMensaje.lote:
            if mensaje.lenguaje == LENGUAJEINGLES and mensaje.fecha <= 2020:
                self.colaRespuestas.send(Respuesta1MensajeSistema(loteMensaje.clienteId, mensaje.url, mensaje.fecha).aBytes())
            if mensaje.fecha <= 2020 and (("biography" in mensaje.seccion.lower()) or ("biographie" in mensaje.seccion)):
                self.colaImgDowloader.send(ImgMensajeSistema(loteMensaje.clienteId, mensaje.url, mensaje.nombre))
            self.colaTransformador.send(TransformadorMensajeSistema(loteMensaje.clienteId, mensaje.url, mensaje.fecha, mensaje.resumen, mensaje.lenguaje))
            

    def _procesarEOF(self, mensaje: FinMensajeSistema) -> None:
        self.colaImgDowloader.send(mensaje.aBytes())
        self.colaTransformador.send(mensaje.aBytes())


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