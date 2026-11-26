import os
import logging
import signal
import threading
from latido import Latido
from contadorEof import contadorEof
from middleware import MessageMiddlewareQueue
from protocolo.mensajesCliente import LENGUAJEINGLES, LENGUAJEFRANCES
from protocolo.mensajesSistema import recvMensajeSistema, FinMensajeSistema,ClienteMuertoMensajeSistema, LoteDataMensajeSistema, ImgMensajeSistema, ImgLoteMensajeSistema, Respuesta1MensajeSistema, TransformadorMensajeSistema, TransformadorLoteMensajeSistema, ETAPA_CLASIFICADOR, origenGateway


MOMHOST = os.environ["MOMHOST"]
COLADATOS = os.environ["COLADATOS"]
COLARESPUESTAS = os.environ["COLARESPUESTAS"]
COLAIMGDESCARGA = os.environ["COLAIMGDESCARGA"]
COLATRANSFORMADOR = os.environ["COLATRANSFORMADOR"]
TOTALTRANSFORMADORES = int(os.environ["TOTALTRANSFORMADORES"])
TOTALIMGDESCARGADORES = int(os.environ["TOTALIMGDESCARGADORES"])
ID = int(os.environ["ID"])

class Clasificador:
    def __init__(self):
        self.colaDatos = MessageMiddlewareQueue(MOMHOST, COLADATOS + "_" + str(ID))
        self.colaRespuestas = MessageMiddlewareQueue(MOMHOST, COLARESPUESTAS)
        self.colaImgDescarga = [MessageMiddlewareQueue(MOMHOST, COLAIMGDESCARGA + "_" + str(i)) for i in range(TOTALIMGDESCARGADORES)]
        self.colaTransformador = [MessageMiddlewareQueue(MOMHOST, COLATRANSFORMADOR + "_" + str(i)) for i in range(TOTALTRANSFORMADORES)]

        # El unico nodo anterior es el gateway
        self.contador = contadorEof(1)


    def _procesarData(self, loteMensaje: LoteDataMensajeSistema) -> None:
        logging.debug(f"Recibo lote {loteMensaje.secuencia} de {loteMensaje.clienteId}")
        imgMensajes = []
        transformadorMensajes = []
        for indice, mensaje in enumerate(loteMensaje.lote):
            if mensaje.lenguaje == LENGUAJEINGLES and mensaje.fecha <= 2020:
                idRespuesta = (ETAPA_CLASIFICADOR, ID, loteMensaje.secuencia, indice)
                self.colaRespuestas.send(Respuesta1MensajeSistema(loteMensaje.clienteId, mensaje.url, mensaje.fecha, idRespuesta).aBytes())
            if mensaje.fecha <= 2020 and mensaje.biografia == 1:
                imgMensajes.append(ImgMensajeSistema(loteMensaje.clienteId, mensaje.url, mensaje.nombre, mensaje.imgUrl))

            transformadorMensajes.append(TransformadorMensajeSistema(mensaje.url, mensaje.fecha, mensaje.resumen, mensaje.lenguaje))

        particion = loteMensaje.clienteId.int + loteMensaje.secuencia
        self.colaImgDescarga[particion % TOTALIMGDESCARGADORES].send(ImgLoteMensajeSistema(loteMensaje.clienteId, imgMensajes, loteMensaje.secuencia).aBytes())
        self.colaTransformador[particion % TOTALTRANSFORMADORES].send(TransformadorLoteMensajeSistema(loteMensaje.clienteId, transformadorMensajes, loteMensaje.secuencia).aBytes())


    def _finalizarCliente(self, fin: FinMensajeSistema) -> None:
        clienteId = fin.clienteId
        self.colaRespuestas.send(FinMensajeSistema(clienteId, origen=origenGateway(ETAPA_CLASIFICADOR, ID)).aBytes())

        logging.info(f"Mando EOF de {clienteId} con total {fin.totalMsg}")
        for cola in self.colaImgDescarga + self.colaTransformador:
            cola.send(FinMensajeSistema(clienteId, fin.totalMsg, ID).aBytes())
        self.contador.finalizar(clienteId)


    def procesarMensaje(self, bytes, ack, nack):
        try:
            mensaje = recvMensajeSistema(bytes)
            if isinstance(mensaje, FinMensajeSistema):
                if self.contador.eofRecibido(mensaje.clienteId, mensaje.origen):
                    self._finalizarCliente(mensaje)
            elif self.contador.yaFinalizado(mensaje.clienteId):
                logging.info(f"Descarto lote {mensaje.secuencia} de {mensaje.clienteId}: cliente ya finalizado")
            elif self.contador.yaProcesado(mensaje.clienteId, mensaje.secuencia):
                logging.info(f"Descarto lote {mensaje.secuencia} de {mensaje.clienteId}: duplicado")
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

        latido = Latido(self.colaDatos.connection)
        thread_latido = threading.Thread(target=latido.start, daemon=True)
        thread_latido.start()


        self.colaDatos.start_consuming(self.procesarMensaje)
        self._close_connections()


    def manejarSigterm(self) -> None:
        self.colaDatos.remote_stop() #mando la señal para que el hilo que maneja corte el channel esto vuelve a lo
                                     #que va despues de invocar al hilo en iniciar

    def _close_connections(self):
        self.colaDatos.close()
        self.colaRespuestas.close()
        for cola in self.colaImgDescarga + self.colaTransformador:
            cola.close()



def main() -> int:
    logging.basicConfig(level=logging.INFO)
    clasificador = Clasificador()
    signal.signal(signal.SIGTERM, lambda signum, frame: clasificador.manejarSigterm())
    clasificador.iniciar()
    return 0


if __name__ == "__main__":
    main()
