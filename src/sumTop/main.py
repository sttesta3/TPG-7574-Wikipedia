import os
import uuid
import signal
import logging
import traceback
import threading
from latido import Latido
from wal import Wal, LineaLog
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


class WalSumtop(Wal):
    def __init__(self):
        super().__init__()


    def guardarEstado(self, estado: dict[uuid.UUID,  dict[str,int]]):
        self.wal_log(LineaLog.STARTCHECKPOINT)
        
        tmp = open("tmp", "a")

        for cliente, palabras in estado.items():
            tmp.write(str(cliente) + ":")
            for palabra, cantidad in palabras.items():
                tmp.write("|" +palabra + ":" + cantidad)
            tmp.write("\n")
        
        tmp.flush()
        tmp.close()
        os.replace("tmp", "checkpoint")

        self.wal_log(LineaLog.ENDCHECKPOINT)


    def recuperarEstado(self) -> dict[uuid.UUID,  dict[str,int]]:
        
        rta = {}
        
        with open("estado", "r") as f:
            for line in f.readlines():

                splited  = line.split(":|")
                clienteId = uuid.UUID(splited[0])
                
                for x in splited[1].split("|"):
                    palabra, cantidad = x.split(":", 1)
                    rta[clienteId][palabra] = cantidad
                        
        return rta


class SumTop:
    def __init__(self):
        self.colaSumTop = MessageMiddlewareQueue(MOMHOST, COLASUMTOP + "_" + ID)
        self.colaTopParcial = [MessageMiddlewareQueue(MOMHOST, COLATOPPARCIAL + "_" + str(i)) for i in range(TOTALTOPPARCIAL)]

        self.contador = contadorEof(TOTALTRANSFORMADORES)

        self.clientes = {}
        self.wal = WalSumtop()


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

       #del self.clientes[clienteId]
       # self.wal.borrarLog(clienteId)
        logging.debug(f"Mando parciales y EOF de {clienteId}")


    def procesarMensaje(self, bytes, ack, nack):
        try:
            mensaje = recvMensajeSistema(bytes)
            #self.wal.guardarMensaje(bytes)
            if isinstance(mensaje, FinMensajeSistema):
                if self.contador.eofRecibido(mensaje.clienteId, mensaje.origen):
                    self._finalizarCliente(mensaje.clienteId)
                    self.contador.finalizar(mensaje.clienteId)
            elif self.contador.yaFinalizado(mensaje.clienteId):
                logging.info(f"Descarto lote {mensaje.secuencia} de {mensaje.clienteId}: cliente ya finalizado")
            elif self.contador.yaProcesado(mensaje.clienteId, mensaje.secuencia):
                logging.info(f"Descarto lote {mensaje.secuencia} de {mensaje.clienteId}: duplicado")
                logging.debug(f"Descarto lote {mensaje.secuencia} de {mensaje.clienteId}: cliente ya finalizado")
            elif isinstance(mensaje, ClienteMuertoMensajeSistema):
                for i in range(TOTALTOPPARCIAL):
                    self.excahangeTopParciales[i].send(bytes)
                #del self.clientes[mensaje.clienteId]
            else:
                self.contador.procesado(mensaje.clienteId, mensaje.secuencia)
                self._procesarData(mensaje)
            ack()
        except Exception as e:
            logging.warning(e)
            logging.warning(traceback.format_exc())
            nack()


    def _recuperarLog(self):
        for log in self.wal.recuperarMensajes():
            if isinstance(log, FinMensajeSistema):
                self.contador.eofRecibido(log)
            elif self.contador.yaFinalizado(log.clienteId):
                logging.debug(f"Descarto lote {log.secuencia} de {log.clienteId}: cliente ya finalizado")
            else:
                self.contador.procesado(log.clienteId, log.secuencia)
                self._procesarData(log)


    def iniciar(self):
        latido = Latido(self.colaSumTop.connection)
        thread_latido = threading.Thread(target=latido.start, daemon=True)
        thread_latido.start()

        self._recuperarLog()
        
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
