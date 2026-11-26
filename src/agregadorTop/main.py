import os
import signal
import logging
import traceback
import threading
from latido import Latido
from contadorEof import contadorEof
from wal import Wal, LineaLog, Recipient
from middleware import MessageMiddlewareQueue
from protocolo.mensajesSistema import recvMensajeSistema, FinMensajeSistema, PalabrasLoteMensajeSistema, PalabrasMensajeSistema, Respuesta3MensajeSistema, ETAPA_AGREGADOR, origenGateway, ClienteMuertoMensajeSistema

MOMHOST = os.environ["MOMHOST"]
COLASUMTOP = os.environ["COLASUMTOP"]
COLARESPUESTAS = os.environ["COLARESPUESTAS"]
COLATOPPARCIAL = os.environ["COLATOPPARCIAL"]
COLATOPGLOBAL = os.environ["COLATOPGLOBAL"]
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
    def __init__(self):
        super().__init__()

    def recuperarEstado(self):
        # Misma operacion que guardarEstado
        # Nota: Si no esta la linea 2. ,el checkpoint es invalido y debes recrear el estado desde el estado anterior + mensajes 
        #       Si esta la linea 2. , es valido y tenes que ejecutar 3-4-5 y seguir con tu vida 
        pass

class AgregadorTop:
    def __init__(self):
        self.colaTopParcial = MessageMiddlewareQueue(MOMHOST, COLATOPPARCIAL + "_" + str(ID))
        self.colaTopGlobal = [MessageMiddlewareQueue(MOMHOST, COLATOPGLOBAL + "_" + str(i)) for i in range(TOTALTOPGLOBAL)]
        self.colaRespuestas = MessageMiddlewareQueue(MOMHOST, COLARESPUESTAS)
         
        self.clientes = {}
        self.contador = contadorEof(TOTALSUMTOP)
        self.wal = WalAgregadorTop()


    def _procesarData(self, mensajes: PalabrasLoteMensajeSistema) -> None:
        mensaje = mensajes.mensajes[0]
        clienteId = mensajes.clienteId
        if clienteId not in self.clientes:
            self.clientes[clienteId] = PalabrasPorIdioma()

        duplicadas = []
        tanda = 0
        for clave, valor in mensaje.palabras.items():
            #self.wal.log(LineaLog.REDOLOG, f"{clienteId},add,{clave},{valor},{mensaje.lenguaje}")
            if self.clientes[clienteId].add(palabra=clave, cantidad=valor, lenguaje=mensaje.lenguaje):
                # Palabra duplicada.
                duplicadas.append(clave)
                if len(duplicadas) == LOTE:
                    idRespuesta = (ETAPA_AGREGADOR, int(ID), mensajes.secuencia, tanda)
                    self.wal.guardarMensaje(mensaje, Recipient.COLARESPUESTAS)
                    self.colaRespuestas.send(Respuesta3MensajeSistema(clienteId, duplicadas, idRespuesta).aBytes())
                    duplicadas = []
                    tanda += 1
        #self.wal.log(LineaLog.REDOLOG, f"{clienteId},FINLOTE")
        if len(duplicadas) > 0:
            idRespuesta = (ETAPA_AGREGADOR, int(ID), mensajes.secuencia, tanda)
            self.wal.guardarMensaje(mensaje, Recipient.COLARESPUESTAS)
            self.colaRespuestas.send(Respuesta3MensajeSistema(clienteId, duplicadas, idRespuesta).aBytes())


    def _top20(self, palabras: dict[str, int]) -> dict[str, int]:
        top = sorted(palabras.items(), key=lambda item: item[1], reverse=True)
        return dict(top[:TOP_SIZE])

    def _procesarEOF(self, mensaje: FinMensajeSistema) -> None:
        if self.contador.eofRecibido(mensaje.clienteId, mensaje.origen):
            palabras = self.clientes.pop(mensaje.clienteId, PalabrasPorIdioma())
            self.wal.guardarMensaje(mensaje, Recipient.COLARESPUESTAS)
            self.colaRespuestas.send(FinMensajeSistema(mensaje.clienteId, origen=origenGateway(ETAPA_AGREGADOR, int(ID))).aBytes())

            nodo = mensaje.clienteId.int % TOTALTOPGLOBAL
            self.colaTopGlobal[nodo].send(PalabrasLoteMensajeSistema(mensaje.clienteId, [PalabrasMensajeSistema( palabras=self._top20(palabras.mergeTop()), url="", lenguaje=0)], int(ID)).aBytes())
            self.wal.guardarMensaje(mensaje, Recipient.EXCHANGETOPGLOBAL)
            self.colaTopGlobal[nodo].send(FinMensajeSistema(mensaje.clienteId, origen=int(ID)).aBytes())

            self.contador.finalizar(mensaje.clienteId)
            #self.wal.log(LineaLog.FINEOF,f"{mensaje.clienteId}")
            # del self.clientes[mensaje.clienteId]
            
    def procesarMensaje(self, bytes, ack, nack):
        try:
            mensaje = recvMensajeSistema(bytes)
            if isinstance(mensaje, FinMensajeSistema):
                self._procesarEOF(mensaje)
            elif self.contador.yaFinalizado(mensaje.clienteId):
                logging.info(f"Descarto parcial de {mensaje.clienteId}: cliente ya finalizado")
            elif self.contador.yaProcesado(mensaje.clienteId, mensaje.secuencia):
                logging.info(f"Descarto parcial {mensaje.secuencia} de {mensaje.clienteId}: duplicado")
            elif isinstance(mensaje, ClienteMuertoMensajeSistema):
                for i in range(TOTALTOPGLOBAL):
                    self.colaTopGlobal[i].send(bytes)
                    self.colaTopParcial.send(bytes)
                # del self.clientes[mensaje.clienteId]
            else:
                self._procesarData(mensaje)
                self.contador.procesado(mensaje.clienteId, mensaje.secuencia)
            ack()

            if self.wal.tiempoDeCheckpoint():
                #self.wal.log(LineaLog.STARTCHECKPOINT)
                self.guardarEstado(self.devolverEstado())
                #self.wal.log(LineaLog.OKCHECKPOINT)
                self.wal.estadoTemporalAPermanente()
                #self.wal.log(LineaLog.ENDCHECKPOINT)
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
        for log in self.wal.recuperarMensajes():
            if isinstance(log, FinMensajeSistema):
                self._procesarEOF(log)
            else:
                self._procesarData(log)

    def _recuperarEstado(self):
        pass

    def iniciar(self):
        
        self._recuperarEstado()
        
        latido = Latido(self.colaTopParcial.connection)
        thread_latido = threading.Thread(target=latido.start, daemon=True)
        thread_latido.start()

        self.colaTopParcial.start_consuming(self.procesarMensaje)
        self._close_connections()


    def manejarSigterm(self) -> None:
        self.colaTopParcial.remote_stop()


    def _close_connections(self):
        self.colaTopParcial.close()
        for cola in self.colaTopGlobal:
            cola.close()


def main() -> int:
    logging.basicConfig(level=logging.INFO)
    agregadorTop = AgregadorTop()
    signal.signal(signal.SIGTERM, lambda signum, frame: agregadorTop.manejarSigterm())
    agregadorTop.iniciar()
    return 0


if __name__ == "__main__":
    main()
