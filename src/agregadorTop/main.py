import os
import sys
import logging
import signal
import traceback
from middleware import MessageMiddlewareQueue, MessageMiddlewareExchange
from protocolo.mensajesSistema import recvMensajeSistema, FinMensajeSistema, PalabrasMensajeSistema, Respuesta3MensajeSistema


MOMHOST = os.environ["MOMHOST"]
COLASUMTOP = os.environ["COLASUMTOP"]
COLARESPUESTAS = os.environ["COLARESPUESTAS"]
EXCHANGETOPPARCIAL = os.environ["EXCHANGETOPPARCIAL"]
EXCHANGETOPGLOBAL = os.environ["EXCHANGETOPGLOBAL"]
TOTALSUMTOP = int(os.environ["TOTALSUMTOP"])
TOTALTOPGLOBAL = int(os.environ["TOTALTOPGLOBAL"])
TOP_SIZE=20
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
    
class AgregadorTop:
    def __init__(self):
        self.exchangeTopParcial = MessageMiddlewareExchange(MOMHOST, EXCHANGETOPPARCIAL, [EXCHANGETOPPARCIAL+"_"+str(ID)])
        self.exchangeTopGlobal = []
        for i in range(TOTALTOPGLOBAL):
            self.exchangeTopGlobal.append(MessageMiddlewareExchange(MOMHOST, EXCHANGETOPGLOBAL, [EXCHANGETOPGLOBAL+"_"+str(i)]))
        self.colaRespuestas = MessageMiddlewareQueue(MOMHOST, COLARESPUESTAS)
         
        self.clientes = {}


    def _procesarData(self, mensaje: PalabrasMensajeSistema) -> None:
        if mensaje.clienteId not in self.clientes:
            self.clientes[mensaje.clienteId] = [0, PalabrasPorIdioma()]
            
        for clave, valor in mensaje.palabras.items():
            if self.clientes[mensaje.clienteId][1].add(palabra=clave, cantidad=valor, lenguaje=mensaje.lenguaje):
                # Palabra duplicada. Implementacion tipo "streaming"
                self.colaRespuestas.send(Respuesta3MensajeSistema(clienteId=mensaje.clienteId, palabras=[clave]).aBytes())
        
    def _top20(self, palabras: dict[str, int]) -> dict[str, int]:
        top = sorted(palabras.items(), key=lambda item: item[1], reverse=True)
        return dict(top[:TOP_SIZE])

    def _procesarEOF(self, mensaje: FinMensajeSistema) -> None:
        self.clientes[mensaje.clienteId][0] += 1
        if self.clientes[mensaje.clienteId][0] == TOTALSUMTOP:
#            logging.info(self._top20(self.clientes[mensaje.clienteId][1]))

            nodo = mensaje.clienteId.int % TOTALTOPGLOBAL
            self.exchangeTopGlobal[nodo].send(PalabrasMensajeSistema(clienteId=mensaje.clienteId, palabras=self._top20(self.clientes[mensaje.clienteId][1].mergeTop()), url="", lenguaje=0).aBytes())    
            self.exchangeTopGlobal[nodo].send(FinMensajeSistema(mensaje.clienteId).aBytes())
            
            del self.clientes[mensaje.clienteId]
            

    def procesarMensaje(self, bytes, ack, nack):
        try:
            mensaje = recvMensajeSistema(bytes)
            if isinstance(mensaje, FinMensajeSistema): # TODO: esta bien esto?
                self._procesarEOF(mensaje)
            else:
                self._procesarData(mensaje)
            ack()
        except Exception as e:
            logging.warning(e)
            logging.warning(traceback.format_exc())
            nack()

    def iniciar(self):
        self.exchangeTopParcial.start_consuming(self.procesarMensaje)


    def manejarSigterm(self) -> None:
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
