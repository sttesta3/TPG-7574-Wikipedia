import os
import sys
import signal
import threading
from mensajesSistema import recvMensajeSistema, FinMensajeSistema, LoteDataMensajeSistema, ImgMensajeSistema, Respuesta1MensajeSistema, TransformadorMensajeSistema
from middleware import MessageMiddlewareQueue,MessageMiddlewareExchange

MOMHOST = os.environ["MOMHOST"]
COLADATOS = os.environ["COLADATOS"]
COLARESPUESTAS = os.environ["COLARESPUESTAS"]
COLAIMGDESCARGA = os.environ["COLAIMGDESCARGA"]
COLATRANSFORMADOR = os.environ["COLATRANSFORMADOR"]

LENGUAJEINGLES = 1

class ClienteLock():
    def __init__(self) -> None:
        self.cond = threading.Condition()
        self.eof = False
        self.respuestas = 0

    def nuevoMensaje(self) -> None:
        with self.cond:
            self.respuestas += 1


    def nuevaRespuesta(self):
        with self.cond:
            self.respuestas -= 1
            if self.respuestas <= 0 and self.eof:
                self.cond.notify_all()
            

    def llegadaEof(self):
        with self.cond:
            self.eof = True
            while self.respuestas > 0:
                self.cond.wait()
    

class Clasificador:
    def __init__(self):
        self.colaDatos = MessageMiddlewareQueue(MOMHOST, COLADATOS)
        self.colaRespuestas = MessageMiddlewareQueue(MOMHOST, COLARESPUESTAS)
        self.colaImgDescarga = MessageMiddlewareQueue(MOMHOST, COLAIMGDESCARGA)
        self.colaTransformador = MessageMiddlewareQueue(MOMHOST, COLATRANSFORMADOR)

        self.colaEOF = MessageMiddlewareExchange(MOMHOST, "EOF", ["EOF"])
        self.colaEOFSend = MessageMiddlewareExchange(MOMHOST, "EOF", ["EOF"])

        self.clientes = {}


    def _procesarData(self, loteMensaje: LoteDataMensajeSistema) -> None:
        if loteMensaje.clienteId not in self.clientes:
            self.clientes[loteMensaje.clienteId] = ClienteLock()

        self.clientes[loteMensaje.clienteId].nuevoMensaje()
         
        for mensaje in loteMensaje.lote:
            if mensaje.lenguaje == LENGUAJEINGLES and mensaje.fecha <= 2020:
                self.colaRespuestas.send(Respuesta1MensajeSistema(loteMensaje.clienteId, mensaje.url, mensaje.fecha).aBytes())
            if mensaje.fecha <= 2020 and mensaje.biografia == 1:
                self.colaImgDescarga.send(ImgMensajeSistema(loteMensaje.clienteId, mensaje.url, mensaje.nombre, mensaje.imgUrl).aBytes())
            self.colaTransformador.send(TransformadorMensajeSistema(loteMensaje.clienteId, mensaje.url, mensaje.fecha, mensaje.resumen, mensaje.lenguaje).aBytes())

        self.clientes[loteMensaje.clienteId].nuevaRespuesta()
            

    def _procesarEOF(self, mensaje: FinMensajeSistema) -> None:
        self.colaEOF.send(mensaje.aBytes())


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


    def _manejarEof(self, bytes, ack, nack):
        try:
            mensaje = recvMensajeSistema(bytes)

            self.clientes[mensaje.clienteId].llegadaEof()
            
            self.colaImgDescarga.send(mensaje.aBytes())
            self.colaTransformador.send(mensaje.aBytes())

            ack()
        except Exception as e:
            print(e)
            nack()

    
    def _controlarEof(self):
        self.colaEOFSend.start_consuming(self._manejarEof)


    def iniciar(self):
        threading.Thread(target=self._controlarEof, daemon=True).start()
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