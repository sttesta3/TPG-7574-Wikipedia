import os
import sys
import logging
import signal
import traceback
from contadorEof import contadorEof
from middleware import MessageMiddlewareQueue
from protocolo.mensajesSistema import recvMensajeSistema, FinMensajeSistema, PalabrasLoteMensajeSistema, PalabrasMensajeSistema

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

        logging.info(f"Mando parciales y EOF de {clienteId}")


    def procesarMensaje(self, bytes, ack, nack):
        try:
            mensaje = recvMensajeSistema(bytes)
            if isinstance(mensaje, FinMensajeSistema):
                if self.contador.eofRecibido(mensaje.clienteId, mensaje.origen):
                    self._finalizarCliente(mensaje.clienteId)
                    self.contador.finalizar(mensaje.clienteId)
            elif self.contador.yaFinalizado(mensaje.clienteId):
                logging.info(f"Descarto lote {mensaje.secuencia} de {mensaje.clienteId}: cliente ya finalizado")
            elif self.contador.yaProcesado(mensaje.clienteId, mensaje.secuencia):
                logging.info(f"Descarto lote {mensaje.secuencia} de {mensaje.clienteId}: duplicado")
            else:
                self._procesarData(mensaje)
                self.contador.procesado(mensaje.clienteId, mensaje.secuencia)
            ack()
        except Exception as e:
            logging.warning(e)
            logging.warning(traceback.format_exc())
            nack()


    def iniciar(self):
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
