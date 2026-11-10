import os
import sys
import signal
import logging
import threading
from contadorDistribuido import contadorDistribuido
from middleware import MessageMiddlewareQueue
from protocolo.mensajesSistema import recvMensajeSistema, FinPromMensajeSistema, CantidadPalabrasLoteMensajeSistema, Respuesta5MensajeSistema, FinMensajeSistema

MOMHOST = os.environ["MOMHOST"]
COLARESPUESTAS = os.environ["COLARESPUESTAS"]
COLACUENTAPROM = os.environ["COLACUENTAPROM"]
EXCHANGECUENTAPROMEOF = os.environ["EXCHANGECUENTAPROMEOF"]
ID = os.environ["ID"]
LOTE = 100


class CuentaProm:
    def __init__(self):
        self.colaRespuestas = MessageMiddlewareQueue(MOMHOST, COLARESPUESTAS)
        self.colaCuentaProm = MessageMiddlewareQueue(MOMHOST, COLACUENTAPROM)

        self.contador = contadorDistribuido(MOMHOST, EXCHANGECUENTAPROMEOF, self._finalizarCliente, self.colaCuentaProm.remote_execution)


    def _procesarData(self, mensajes: CantidadPalabrasLoteMensajeSistema) -> None:
        with open(str(mensajes.clienteId), "a", encoding="utf-8") as f:
            for mensaje in mensajes.mensajes:
                f.write(f"{mensaje.url};;;;;{mensaje.cantidad}\n")


    def _finalizarCliente(self, clienteId, fin: FinPromMensajeSistema, originador: bool) -> None:
        archivo = str(clienteId)
        if os.path.exists(archivo):
            with open(archivo, "r", encoding="utf-8") as f:
                data = {}
                for linea in f.readlines():
                    url, cantidad = linea.strip().split(";;;;;", 1)
                    if int(cantidad) > fin.promedio:
                        data[url] = int(cantidad)
                        if len(data) == LOTE:
                            self.colaRespuestas.send(Respuesta5MensajeSistema(clienteId, data).aBytes())
                            data = {}
                if len(data) > 0:
                    self.colaRespuestas.send(Respuesta5MensajeSistema(clienteId, data).aBytes())
            os.remove(archivo)

        self.colaRespuestas.send(FinMensajeSistema(clienteId).aBytes())
        logging.info(f"Mando EOF de {clienteId}")


    def procesarMensaje(self, bytes, ack, nack):
        try:
            mensaje = recvMensajeSistema(bytes)
            if isinstance(mensaje, FinPromMensajeSistema):
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
        self.colaCuentaProm.start_consuming(self.procesarMensaje)
        thread_contador.join()
        self._close_connections()


    def manejarSigterm(self) -> None:
        self.contador.detener()
        self.colaCuentaProm.remote_stop()


    def _close_connections(self):
        self.colaCuentaProm.close()
        self.colaRespuestas.close()
        self.contador.cerrar()


def main() -> int:
    logging.basicConfig(level=logging.INFO)
    cuentaProm = CuentaProm()
    signal.signal(signal.SIGTERM, lambda signum, frame: cuentaProm.manejarSigterm())
    cuentaProm.iniciar()
    return 0


if __name__ == "__main__":
    main()
