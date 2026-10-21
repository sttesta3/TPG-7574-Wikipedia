import os
import sys
import signal
from mensajesSistema import recvMensajeSistema, FinMensajeSistema, LoteDataMensajeSistema, ImgMensajeSistema, Respuesta1MensajeSistema, TransformadorMensajeSistema
from middleware import MessageMiddlewareQueue

MOMHOST = os.environ["MOMHOST"]
COLADATOS = os.environ["COLADATOS"]
COLARESPUESTAS = os.environ["COLARESPUESTAS"]
COLAIMGDESCARGA = os.environ["COLAIMGDESCARGA"]
COLATRANSFORMADOR = os.environ["COLATRANSFORMADOR"]

LENGUAJEINGLES = 1

class Clasificador:
    def __init__(self):
        self.colaDatos = MessageMiddlewareQueue(MOMHOST, COLADATOS)
        self.colaRespuestas = MessageMiddlewareQueue(MOMHOST, COLARESPUESTAS)
        self.colaImgDescarga = MessageMiddlewareQueue(MOMHOST, COLAIMGDESCARGA)
        self.colaTransformador = MessageMiddlewareQueue(MOMHOST, COLATRANSFORMADOR)


    def _procesarData(self, loteMensaje: LoteDataMensajeSistema) -> None:
        for mensaje in loteMensaje.lote:
            if mensaje.lenguaje == LENGUAJEINGLES and mensaje.fecha <= 2020:
                self.colaImgDescarga.send(ImgMensajeSistema(loteMensaje.clienteId, mensaje.url, mensaje.nombre, mensaje.imgUrl).aBytes())
                self.colaRespuestas.send(Respuesta1MensajeSistema(loteMensaje.clienteId, mensaje.url, mensaje.fecha).aBytes())
            if mensaje.fecha <= 2020 and (("biography" in mensaje.seccion.lower()) or ("biographie" in mensaje.seccion.lower())):
                self.colaImgDescarga.send(ImgMensajeSistema(loteMensaje.clienteId, mensaje.url, mensaje.nombre, mensaje.imgUrl).aBytes())
            self.colaTransformador.send(TransformadorMensajeSistema(loteMensaje.clienteId, mensaje.url, mensaje.fecha, mensaje.resumen, mensaje.lenguaje).aBytes())
            

    def _procesarEOF(self, mensaje: FinMensajeSistema) -> None:
        self.colaImgDescarga.send(mensaje.aBytes())
        self.colaTransformador.send(mensaje.aBytes())


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
            nack()


    def iniciar(self):
        self.colaDatos.start_consuming(self.procesarMensaje)


    def manejarSigterm(self) -> None:
        self.colaDatos.close()
        self.colaRespuestas.close()
        self.colaImgDescarga.close()
        self.colaTransformador.close()
        sys.exit(0)


def main() -> int:
    clasificador = Clasificador()
    signal.signal(signal.SIGTERM, lambda signum, frame: clasificador.manejarSigterm())
    clasificador.iniciar()
    return 0


if __name__ == "__main__":
    main()