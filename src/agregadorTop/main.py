import os
import signal
import logging
import traceback
import threading
from wal import Wal, LineaLog
from latido import Latido
from middleware import MessageMiddlewareQueue, MessageMiddlewareExchange
from protocolo.mensajesSistema import recvMensajeSistema, FinMensajeSistema, PalabrasLoteMensajeSistema, PalabrasMensajeSistema, Respuesta3MensajeSistema


MOMHOST = os.environ["MOMHOST"]
COLASUMTOP = os.environ["COLASUMTOP"]
COLARESPUESTAS = os.environ["COLARESPUESTAS"]
EXCHANGETOPPARCIAL = os.environ["EXCHANGETOPPARCIAL"]
EXCHANGETOPGLOBAL = os.environ["EXCHANGETOPGLOBAL"]
TOTALSUMTOP = int(os.environ["TOTALSUMTOP"])
TOTALTOPGLOBAL = int(os.environ["TOTALTOPGLOBAL"])
TOP_SIZE=20
LOTE = 100
ID = os.environ["ID"]

class PalabrasPorIdioma:
    def __init__(self):
        self.palabras = {}

    def add(self, cantidad: int, lenguaje, palabra: str) -> bool:
        '''
        recibe lenguaje, palabra, cantidad 
        actualiza la lista de palabras y devuelve True para la PRIMERA detección de palabra compartida  
        '''
        duplicada = False
        actual = self.palabras.get(palabra, [0,{}]) # [conteo de apariciones de la palabra, { idioma: 1 } (tabla de hash de idiomas)]
        actual[0] += cantidad
        if not lenguaje in actual[1]:
            actual[1][lenguaje] = 1
            # Nota: Esta pensado para dos idiomas 
            duplicada = len(actual[1]) == 2
        self.palabras[palabra] = actual
        return duplicada

    def mergeTop(self) -> dict[str, int]:
        result = {}
        for clave, valor in self.palabras.items():
            result[clave] = valor[0]
        return result
    

class WalAgregadorTop(Wal):
    def __init__():
        super().__init__()

    def guardarEstado(self):
        # 0. Log checkpoint
        # 1. Guarda todo el estado en un archivo temporal
        # 2. Logea que guardo el estado
        # 3. mv log_temporal log permanante (renombra log_temporal -> log_permanente, borrando el temporal)
        # 4. Borrar mensajes 
        # 5. Log END CHECKPOINT
        self.wal_log(LineaLog.STARTCHECKPOINT)
        
        self.wal_log(LineaLog.ENDCHECKPOINT)
        pass

    def recuperarEstado(self):
        # Misma operacion que guardarEstado
        # Nota: Si no esta la linea 2. ,el checkpoint es invalido y debes recrear el estado desde el estado anterior + mensajes 
        #       Si esta la linea 2. , es valido y tenes que ejecutar 3-4-5 y seguir con tu vida 
        pass

class AgregadorTop:
    def __init__(self):
        self.exchangeTopParcial = MessageMiddlewareExchange(MOMHOST, EXCHANGETOPPARCIAL, [EXCHANGETOPPARCIAL+"_"+str(ID)])
        self.exchangeTopGlobal = []
        for i in range(TOTALTOPGLOBAL):
            self.exchangeTopGlobal.append(MessageMiddlewareExchange(MOMHOST, EXCHANGETOPGLOBAL, [EXCHANGETOPGLOBAL+"_"+str(i)]))
        self.colaRespuestas = MessageMiddlewareQueue(MOMHOST, COLARESPUESTAS)
         
        self.clientes = {}
        self.wal = WalAgregadorTop()


    def _procesarData(self, mensajes: PalabrasLoteMensajeSistema) -> None:
        mensaje = mensajes.mensajes[0]
        clienteId = mensajes.clienteId
        if clienteId not in self.clientes:
            self.clientes[clienteId] = [0, PalabrasPorIdioma()]

        duplicadas = []
        for clave, valor in mensaje.palabras.items():
            if self.clientes[clienteId][1].add(palabra=clave, cantidad=valor, lenguaje=mensaje.lenguaje):
                # Palabra duplicada. 
                duplicadas.append(clave)
                if len(duplicadas) == LOTE:
                    self.colaRespuestas.send(Respuesta3MensajeSistema(clienteId=clienteId, palabras=duplicadas).aBytes())
                    duplicadas = []
        if len(duplicadas) > 0:
            self.colaRespuestas.send(Respuesta3MensajeSistema(clienteId=clienteId, palabras=duplicadas).aBytes())


    def _top20(self, palabras: dict[str, int]) -> dict[str, int]:
        top = sorted(palabras.items(), key=lambda item: item[1], reverse=True)
        return dict(top[:TOP_SIZE])

    def _procesarEOF(self, mensaje: FinMensajeSistema) -> None:
        if mensaje.clienteId not in self.clientes:
            self.clientes[mensaje.clienteId] = [0, PalabrasPorIdioma()]

        self.clientes[mensaje.clienteId][0] += 1
        if self.clientes[mensaje.clienteId][0] == TOTALSUMTOP:
            self.colaRespuestas.send(FinMensajeSistema(mensaje.clienteId).aBytes())

            nodo = mensaje.clienteId.int % TOTALTOPGLOBAL
            self.exchangeTopGlobal[nodo].send(PalabrasLoteMensajeSistema(mensaje.clienteId, [PalabrasMensajeSistema( palabras=self._top20(self.clientes[mensaje.clienteId][1].mergeTop()), url="", lenguaje=0)]).aBytes())    
            self.exchangeTopGlobal[nodo].send(FinMensajeSistema(mensaje.clienteId).aBytes())
            
            self.wal.borrarLog(mensaje.clienteId)
            del self.clientes[mensaje.clienteId]
            

    def procesarMensaje(self, bytes, ack, nack):
        try:
            self.wal.guardarMensaje(bytes)
            ack()   
            # Caso borde en ESTA LINEA: Hice ACK del mensaje y no pude logear el ack. 
            # Al leer log no se si este mensaje sera procesado por otro nodo o no. 
            # Problema sin solucion: Se asume que el proceso de log es inmediato y que esta falla no puede darse
            self.wal.log(LineaLog.RABBITACKMSG)
            mensaje = recvMensajeSistema(bytes)
            if isinstance(mensaje, FinMensajeSistema):
                self._procesarEOF(mensaje)
            else:
                self._procesarData(mensaje)
        except Exception as e:
            logging.warning(e)
            logging.warning(traceback.format_exc())
            self.wal.log(LineaLog.RABBITNACKMSG)
            nack()


    def _recuperarLog(self):
        for log in self.wal.recuperarLogs():
            if isinstance(log, FinMensajeSistema):
                self._procesarEOF(log)
            else:
                self._procesarData(log)


    def iniciar(self):
        self._recuperarLog()
        
        latido = Latido(self.colaDatos.connection)
        thread_latido = threading.Thread(target=latido.start, daemon=True)
        thread_latido.start()

        self.exchangeTopParcial.start_consuming(self.procesarMensaje)
        self._close_connections()



    def manejarSigterm(self) -> None:
        self.exchangeTopParcial.remote_stop()


    def _close_connections(self):
        self.exchangeTopParcial.close()
        for i in range(TOTALTOPGLOBAL):
            self.exchangeTopGlobal[i].close()


def main() -> int:
    logging.basicConfig(level=logging.INFO)
    agregadorTop = AgregadorTop()
    signal.signal(signal.SIGTERM, lambda signum, frame: agregadorTop.manejarSigterm())
    agregadorTop.iniciar()
    return 0


if __name__ == "__main__":
    main()
