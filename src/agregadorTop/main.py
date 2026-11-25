import os
import signal
import logging
import traceback
import threading
from wal import Wal, LineaLog, Recipient
from latido import Latido
from middleware import MessageMiddlewareQueue, MessageMiddlewareExchange
from protocolo.mensajesSistema import recvMensajeSistema, FinMensajeSistema, PalabrasLoteMensajeSistema, PalabrasMensajeSistema, Respuesta3MensajeSistema, ClienteMuertoMensajeSistema


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
    def __init__(self, bytes=None):
        self.palabras = {}
        if bytes:
            for registro in bytes.split('\2'):
                campos = registro.split('\1')
                palabra = campos[0]
                conteo = campos[1]
                idiomas = {}
                for idioma in campos[2:]:
                    idiomas[idioma] = 1
                self.palabras[palabra] = [conteo, idiomas]

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

    def devolverEstado(self) -> bytes:
        # Devuelve bytes para guardar en log. palabra \1 conteo \1 idioma 1 \1 idioma 2 \1 ... \0  
        # \2 es el marcador de nuevo registro y \1 el separador de campos 
        resultado = b''
        for palabra, contador in self.palabras.values():
            apariciones = contador[0]
            resultado += palabra + '\1' + apariciones 
            for idioma in contador[1].keys():
                resultado += '\1' + idioma 
            resultado += '\2'
        return resultado                         


class WalAgregadorTop(Wal):
    def __init__():
        super().__init__()

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
            self.wal.log(LineaLog.REDOLOG, f"{clienteId},add,{clave},{valor},{mensaje.lenguaje}")
            if self.clientes[clienteId][1].add(palabra=clave, cantidad=valor, lenguaje=mensaje.lenguaje):
                # Palabra duplicada. 
                duplicadas.append(clave)
                if len(duplicadas) == LOTE:
                    mensaje = Respuesta3MensajeSistema(clienteId=clienteId, palabras=duplicadas).aBytes()
                    self.wal.guardarMensaje(mensaje, Recipient.COLARESPUESTAS)
                    self.colaRespuestas.send(mensaje)
                    duplicadas = []
        
        self.wal.log(LineaLog.REDOLOG, f"{clienteId},FINLOTE")
        if len(duplicadas) > 0:
            mensaje = Respuesta3MensajeSistema(clienteId=clienteId, palabras=duplicadas).aBytes()
            self.wal.guardarMensaje(mensaje, Recipient.COLARESPUESTAS)
            self.colaRespuestas.send(mensaje)


    def _top20(self, palabras: dict[str, int]) -> dict[str, int]:
        top = sorted(palabras.items(), key=lambda item: item[1], reverse=True)
        return dict(top[:TOP_SIZE])

    def _procesarEOF(self, mensaje: FinMensajeSistema) -> None:
        if mensaje.clienteId not in self.clientes:
            self.clientes[mensaje.clienteId] = [0, PalabrasPorIdioma()]

        self.clientes[mensaje.clienteId][0] += 1
        self.wal.log(LineaLog.RECVEOF,f"{mensaje.clienteId}")
        if self.clientes[mensaje.clienteId][0] == TOTALSUMTOP:
            mensaje_eof = FinMensajeSistema(mensaje.clienteId).aBytes()
            self.wal.guardarMensaje(mensaje_eof, Recipient.COLARESPUESTAS)
            self.colaRespuestas.send(mensaje_eof)

            nodo = mensaje.clienteId.int % TOTALTOPGLOBAL
            mensaje_exchange = PalabrasLoteMensajeSistema(mensaje.clienteId, [PalabrasMensajeSistema( palabras=self._top20(self.clientes[mensaje.clienteId][1].mergeTop()), url="", lenguaje=0)]).aBytes()
            self.wal.guardarMensaje(mensaje_exchange, Recipient.EXCHANGETOPGLOBAL)
            self.exchangeTopGlobal[nodo].send()    

            self.wal.guardarMensaje(mensaje_eof, Recipient.EXCHANGETOPGLOBAL)
            self.exchangeTopGlobal[nodo].send(mensaje_eof)
            
            self.wal.log(LineaLog.FINEOF,f"{mensaje.clienteId}")
            del self.clientes[mensaje.clienteId]
            

    def procesarMensaje(self, bytes, ack, nack):
        try:
            mensaje = recvMensajeSistema(bytes)
            if isinstance(mensaje, FinMensajeSistema):
                self._procesarEOF(mensaje)
            elif isinstance(mensaje, ClienteMuertoMensajeSistema):
                for i in range(EXCHANGETOPGLOBAL):
                    self.exchangeTopGlobal[i].send(bytes)
                del self.clientes[mensaje.clienteId]
            else:
                self._procesarData(mensaje)
            ack()   
            if self.wal.tiempoDeCheckpoint():
                self.wal.log(LineaLog.STARTCHECKPOINT)
                self.guardarEstado(self.devolverEstado())
                self.wal.log(LineaLog.OKCHECKPOINT)
                self.wal.estadoTemporalAPermanente()
                self.wal.log(LineaLog.ENDCHECKPOINT)
                self.wal.truncarRedoLog()
                
        except Exception as e:
            logging.warning(e)
            logging.warning(traceback.format_exc())
            if not self.wal.tiempoDeCheckpoint():
                nack()

    def devolverEstado(self) -> bytes :
        resultado = b""
        for cliente, values in self.clientes.items():            
            conteo_eofs: int = values[0]
            resultado += cliente + '\1' + conteo_eofs + '\1'
            palabras: PalabrasPorIdioma = values[1]
            resultado += palabras.devolverEstado() + '\0'
        return resultado

    def cargarEstado(self, bytes):
        for registro_cliente in bytes.split('\0'):
            campos = registro_cliente.split('\1')
            cliente = campos[0]
            conteo_eofs = campos[1]
            palabras = PalabrasPorIdioma.cargarEstado(campos[2:])
            self.clientes[cliente] = [conteo_eofs, palabras]

    def _recuperarLog(self):
        for log in self.wal.recuperarLogs():
            if isinstance(log, FinMensajeSistema):
                self._procesarEOF(log)
            else:
                self._procesarData(log)


    def iniciar(self):
        self._recuperarLog()
        
        latido = Latido(self.exchangeTopParcial.connection)
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
