import os
import signal
import logging
import threading
from latido import Latido
from contadorEof import contadorEof
from middleware import MessageMiddlewareQueue
from protocolo.mensajesSistema import recvMensajeSistema, FinPromMensajeSistema,ClienteMuertoMensajeSistema, CantidadPalabrasLoteMensajeSistema, Respuesta5MensajeSistema, FinMensajeSistema, ETAPA_CUENTAPROM, origenGateway


MOMHOST = os.environ["MOMHOST"]
COLARESPUESTAS = os.environ["COLARESPUESTAS"]
COLACUENTAPROM = os.environ["COLACUENTAPROM"]
TOTALTRANSFORMADORES = int(os.environ["TOTALTRANSFORMADORES"])
ID = os.environ["ID"]
LOTE = 100


class CuentaProm:
    def __init__(self):
        self.colaRespuestas = MessageMiddlewareQueue(MOMHOST, COLARESPUESTAS)
        self.colaCuentaProm = MessageMiddlewareQueue(MOMHOST, COLACUENTAPROM + "_" + ID)

        self.contador = contadorEof(TOTALTRANSFORMADORES)
        # Para cerrar un cliente hacen falta los EOF de todos los transformadores y el promedio
        self.eofsCompletos = set()
        self.promedios = {}

    # TODO: este no tiene nada en memoria. Con esto alcanza (?
    def _procesarData(self, mensajes: CantidadPalabrasLoteMensajeSistema) -> None:
        with open(str(mensajes.clienteId), "a", encoding="utf-8") as f:
            for mensaje in mensajes.mensajes:
                f.write(f"{mensaje.url};;;;;{mensaje.cantidad}\n")


    def _intentarFinalizar(self, clienteId) -> None:
        if clienteId in self.eofsCompletos and clienteId in self.promedios:
            self.eofsCompletos.discard(clienteId)
            self._finalizarCliente(clienteId, self.promedios.pop(clienteId))
            self.contador.finalizar(clienteId)


    def _finalizarCliente(self, clienteId, fin: FinPromMensajeSistema) -> None:
        archivo = str(clienteId)
        if os.path.exists(archivo):
            with open(archivo, "r", encoding="utf-8") as f:
                data = {}
                tanda = 0
                for linea in f.readlines():
                    url, cantidad = linea.strip().split(";;;;;", 1)
                    if int(cantidad) > fin.promedio:
                        data[url] = int(cantidad)
                        if len(data) == LOTE:
                            idRespuesta = (ETAPA_CUENTAPROM, int(ID), 0, tanda)
                            self.colaRespuestas.send(Respuesta5MensajeSistema(clienteId, data, idRespuesta).aBytes())
                            data = {}
                            tanda += 1
                if len(data) > 0:
                    idRespuesta = (ETAPA_CUENTAPROM, int(ID), 0, tanda)
                    self.colaRespuestas.send(Respuesta5MensajeSistema(clienteId, data, idRespuesta).aBytes())
            os.remove(archivo)

        self.colaRespuestas.send(FinMensajeSistema(clienteId, origen=origenGateway(ETAPA_CUENTAPROM, int(ID))).aBytes())
        logging.info(f"Mando EOF de {clienteId}")


    def procesarMensaje(self, bytes, ack, nack):
        try:
            mensaje = recvMensajeSistema(bytes)
            if self.contador.yaFinalizado(mensaje.clienteId):
                logging.info(f"Descarto mensaje de {mensaje.clienteId}: cliente ya finalizado")
            elif isinstance(mensaje, FinPromMensajeSistema):
                self.promedios[mensaje.clienteId] = mensaje
                self._intentarFinalizar(mensaje.clienteId)
            elif isinstance(mensaje, FinMensajeSistema):
                if self.contador.eofRecibido(mensaje.clienteId, mensaje.origen):
                    self.eofsCompletos.add(mensaje.clienteId)
                    self._intentarFinalizar(mensaje.clienteId)
            elif self.contador.yaProcesado(mensaje.clienteId, mensaje.secuencia):
                logging.info(f"Descarto lote {mensaje.secuencia} de {mensaje.clienteId}: duplicado")
            elif isinstance(mensaje, ClienteMuertoMensajeSistema):
                os.remove(str(mensaje.clienteId))
            else:
                self._procesarData(mensaje)
                self.contador.procesado(mensaje.clienteId, mensaje.secuencia)
            ack()
        except Exception as e:
            logging.info(e)
            nack()


    def iniciar(self):
        latido = Latido(self.colaCuentaProm.connection)
        thread_latido = threading.Thread(target=latido.start, daemon=True)
        thread_latido.start()

        thread_contador = threading.Thread(target=self.contador.iniciar, daemon=True)
        thread_contador.start()

        self.colaCuentaProm.start_consuming(self.procesarMensaje)
        self._close_connections()


    def manejarSigterm(self) -> None:
        self.colaCuentaProm.remote_stop()


    def _close_connections(self):
        self.colaCuentaProm.close()
        self.colaRespuestas.close()


def main() -> int:
    logging.basicConfig(level=logging.INFO)
    cuentaProm = CuentaProm()
    signal.signal(signal.SIGTERM, lambda signum, frame: cuentaProm.manejarSigterm())
    cuentaProm.iniciar()
    return 0


if __name__ == "__main__":
    main()
