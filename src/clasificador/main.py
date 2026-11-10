import os
import sys
import logging
import signal
import threading
from contadorDistribuido import contadorDistribuido
from middleware import MessageMiddlewareQueue
from protocolo.mensajesSistema import recvMensajeSistema, FinMensajeSistema, LoteDataMensajeSistema, ImgMensajeSistema, ImgLoteMensajeSistema, Respuesta1MensajeSistema, TransformadorMensajeSistema, TransformadorLoteMensajeSistema
from protocolo.mensajesCliente import LENGUAJEINGLES, LENGUAJEFRANCES

MOMHOST = os.environ["MOMHOST"]
COLADATOS = os.environ["COLADATOS"]
COLARESPUESTAS = os.environ["COLARESPUESTAS"]
COLAIMGDESCARGA = os.environ["COLAIMGDESCARGA"]
COLATRANSFORMADOR = os.environ["COLATRANSFORMADOR"]
CLASIFICADOREXCHANGEEOF = os.environ["CLASIFICADOREXCHANGEEOF"]

class Clasificador:
    def __init__(self):
        self.colaDatos = MessageMiddlewareQueue(MOMHOST, COLADATOS)
        self.colaRespuestas = MessageMiddlewareQueue(MOMHOST, COLARESPUESTAS)
        self.colaImgDescarga = MessageMiddlewareQueue(MOMHOST, COLAIMGDESCARGA)
        self.colaTransformador = MessageMiddlewareQueue(MOMHOST, COLATRANSFORMADOR)

        self.contador = contadorDistribuido(MOMHOST, CLASIFICADOREXCHANGEEOF, self._finalizarCliente, self.colaDatos.remote_execution)


    def _procesarData(self, loteMensaje: LoteDataMensajeSistema) -> None:
        logging.info(f"Recibo lote {loteMensaje.secuencia} de {loteMensaje.clienteId}")
        imgMensajes = []
        transformadorMensajes = []
        for mensaje in loteMensaje.lote:
            if mensaje.lenguaje == LENGUAJEINGLES and mensaje.fecha <= 2020:
                self.colaRespuestas.send(Respuesta1MensajeSistema(loteMensaje.clienteId, mensaje.url, mensaje.fecha).aBytes())
            if mensaje.fecha <= 2020 and mensaje.biografia == 1:
                imgMensajes.append(ImgMensajeSistema(loteMensaje.clienteId, mensaje.url, mensaje.nombre, mensaje.imgUrl))

            transformadorMensajes.append(TransformadorMensajeSistema(mensaje.url, mensaje.fecha, mensaje.resumen, mensaje.lenguaje))

        self.colaImgDescarga.send(ImgLoteMensajeSistema(loteMensaje.clienteId, imgMensajes, loteMensaje.secuencia).aBytes())
        self.colaTransformador.send(TransformadorLoteMensajeSistema(loteMensaje.clienteId, transformadorMensajes, loteMensaje.secuencia).aBytes())


    def _finalizarCliente(self, clienteId, fin: FinMensajeSistema, originador: bool) -> None:
        self.colaRespuestas.send(FinMensajeSistema(clienteId).aBytes())

        if originador:
            logging.info(f"Mando EOF de {clienteId} con total {fin.totalMsg}")
            self.colaImgDescarga.send(FinMensajeSistema(clienteId, fin.totalMsg).aBytes())
            self.colaTransformador.send(FinMensajeSistema(clienteId, fin.totalMsg).aBytes())


    def procesarMensaje(self, bytes, ack, nack):
        try:
            mensaje = recvMensajeSistema(bytes)
            if isinstance(mensaje, FinMensajeSistema):
                self.contador.eofRecibido(mensaje)
            elif self.contador.yaFinalizado(mensaje.clienteId):
                logging.info(f"Descarto lote {mensaje.secuencia} de {mensaje.clienteId}: cliente ya finalizado")
            else:
                self._procesarData(mensaje)
                self.contador.procesado(mensaje.clienteId, mensaje.secuencia)
            ack()
        except Exception as e:
            logging.info(e)
            nack()


    def iniciar(self):
        thread_contador = threading.Thread(target=self.contador.iniciar, daemon=True)
        thread_contador.start()
        self.colaDatos.start_consuming(self.procesarMensaje)
        thread_contador.join()
        self._close_connections()


    def manejarSigterm(self) -> None:
        self.contador.detener()
        self.colaDatos.remote_stop() #mando la señal para que el hilo que maneja corte el channel esto vuelve a lo
                                     #que va despues de invocar al hilo en iniciar

    def _close_connections(self):
        self.colaDatos.close()
        self.colaRespuestas.close()
        self.colaImgDescarga.close()
        self.colaTransformador.close()
        self.contador.cerrar()



def main() -> int:
    logging.basicConfig(level=logging.INFO)
    clasificador = Clasificador()
    signal.signal(signal.SIGTERM, lambda signum, frame: clasificador.manejarSigterm())
    clasificador.iniciar()
    return 0


if __name__ == "__main__":
    main()
