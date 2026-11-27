import os
import signal
import logging
import traceback
import threading
from latido import Latido
from wal import Wal
from contadorEof import contadorEof
from middleware import MessageMiddlewareQueue
from protocolo.mensajesSistema import recvMensajeSistema, FinMensajeSistema, PalabrasLoteMensajeSistema, PalabrasMensajeSistema, ClienteMuertoMensajeSistema


MOMHOST = os.environ["MOMHOST"]
COLASUMTOP = os.environ["COLASUMTOP"]
TOTALTRANSFORMADORES = int(os.environ["TOTALTRANSFORMADORES"])
COLATOPPARCIAL = os.environ["COLATOPPARCIAL"]
TOTALTOPPARCIAL = int(os.environ["TOTALTOPPARCIAL"])
ID = os.environ["ID"]
CANT_LENGUAJES = 2


class SumTop:
    def __init__(self):
        self.colaSumTop = MessageMiddlewareQueue(MOMHOST, COLASUMTOP + "_" + ID)
        self.colaTopParcial = [MessageMiddlewareQueue(MOMHOST, COLATOPPARCIAL + "_" + str(i)) for i in range(TOTALTOPPARCIAL)]

        self.contador = contadorEof(TOTALTRANSFORMADORES)

        self.clientes = {}
        self.wal = Wal()


    def _procesarData(self, mensajes: PalabrasLoteMensajeSistema) -> None:
        clienteId = mensajes.clienteId
        if clienteId not in self.clientes:
            self.clientes[clienteId] = {}

        for mensaje in mensajes.mensajes:
            if mensaje.lenguaje not in self.clientes[clienteId]:
                self.clientes[clienteId][mensaje.lenguaje] = {}

            for clave, valor in mensaje.palabras.items():
                self.clientes[clienteId][mensaje.lenguaje][clave] = self.clientes[clienteId][mensaje.lenguaje].get(clave, 0) + valor


    def _finalizarCliente(self, clienteId) -> None:
        palabrasCliente = self.clientes.pop(clienteId, {})

        nodos = [{} for _ in range(TOTALTOPPARCIAL)]
        for lenguaje, palabras in palabrasCliente.items():
            for clave, valor in palabras.items():
                i = int.from_bytes(clave.encode("UTF-8")) % TOTALTOPPARCIAL
                nodos[i][lenguaje] = nodos[i].get(lenguaje, {})
                nodos[i][lenguaje][clave] = nodos[i][lenguaje].get(clave,valor)

        for i in range(TOTALTOPPARCIAL):
            for lenguaje, palabras in nodos[i].items():
                # La secuencia identifica (nodo, lenguaje), para que el agregador descarte parciales duplicados
                secuencia = int(ID) * CANT_LENGUAJES + lenguaje
                parcial = PalabrasLoteMensajeSistema(clienteId=clienteId, mensajes=[PalabrasMensajeSistema(palabras=palabras, url="", lenguaje=lenguaje)], secuencia=secuencia)
                self.colaTopParcial[i].send(parcial.aBytes())
            self.colaTopParcial[i].send(FinMensajeSistema(clienteId, origen=int(ID)).aBytes())

        logging.debug(f"Mando parciales y EOF de {clienteId}")


    def procesarMensaje(self, bytes, ack, nack):
        try:
            mensaje = recvMensajeSistema(bytes)
            self.wal.guardarMensaje(bytes)

            if isinstance(mensaje, FinMensajeSistema):
                if self.contador.eofRecibido(mensaje.clienteId, mensaje.origen):
                    self._finalizarCliente(mensaje.clienteId)
                    self.contador.finalizar(mensaje.clienteId)
            elif isinstance(mensaje, ClienteMuertoMensajeSistema):
                for i in range(TOTALTOPPARCIAL):
                    self.excahangeTopParciales[i].send(bytes)
                del self.clientes[mensaje.clienteId]
            elif self.contador.yaFinalizado(mensaje.clienteId) or self.contador.yaProcesado(mensaje.clienteId, mensaje.secuencia):
                logging.debug(f"Descarto lote {mensaje.secuencia} de {mensaje.clienteId}: cliente ya finalizado")
            else:
                self.contador.procesado(mensaje.clienteId, mensaje.secuencia)
                self._procesarData(mensaje)
            ack()

            if self.wal.tiempoDeCheckpoint():
                self.wal.guardarEstado(self.clientes, self.contador.state())


        except Exception as e:
            print(e)
            print(f"{traceback.format_exc()}")
            logging.error(e)
            logging.error(traceback.format_exc())
            nack()


    def _recuperarse(self):
        try:
            self.clientes, contador = self.wal.recuperarEstado()
            self.contador.load_state(contador)

            print(self.clientes)

            print(self.contador)

            for logBytes in self.wal.recuperarMensajes():
                
                log = recvMensajeSistema(logBytes)
                if self.contador.yaFinalizado(log.clienteId) or self.contador.yaProcesado(log.clienteId, log.secuencia):
                    logging.debug(f"Descarto lote {log.secuencia} de {log.clienteId}")
                elif isinstance(log, FinMensajeSistema):
                    self.contador.eofRecibido(log)
                else:
                    self.contador.procesado(log.clienteId, log.secuencia)
                    self._procesarData(log)
        except Exception as e:
            print(logBytes)
            print(f"adad{e}")
            print(traceback.format_exc())

    def iniciar(self):
        latido = Latido(self.colaSumTop.connection)
        thread_latido = threading.Thread(target=latido.start, daemon=True)
        thread_latido.start()

        self._recuperarse()

        self.colaSumTop.start_consuming(self.procesarMensaje)
        self._close_connections()


    def manejarSigterm(self) -> None:
        self.colaSumTop.remote_stop()


    def _close_connections(self):
        self.colaSumTop.close()
        for i in range(TOTALTOPPARCIAL):
            self.colaTopParcial[i].close()



def main() -> int:
    logging.basicConfig(level=logging.INFO)
    sumTop = SumTop()
    signal.signal(signal.SIGTERM, lambda signum, frame: sumTop.manejarSigterm())
    sumTop.iniciar()
    return 0


if __name__ == "__main__":
    main()
