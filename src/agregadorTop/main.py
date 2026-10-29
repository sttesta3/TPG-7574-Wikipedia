import os
import sys
import signal
from protocolo.mensajesSistema import recvMensajeSistema, FinMensajeSistema, TransformadorMensajeSistema, PalabrasMensajeSistema, CantidadPalabraMensajeSistema, Respuesta3MensajeSistema
from middleware import MessageMiddlewareQueue, MessageMiddlewareExchange

import traceback

MOMHOST = os.environ["MOMHOST"]
COLASUMTOP = os.environ["COLASUMTOP"]
COLARESPUESTAS = os.environ["COLARESPUESTAS"]
EXCHANGETOPPARCIAL = os.environ["EXCHANGETOPPARCIAL"]
EXCHANGETOPGLOBAL = os.environ["EXCHANGETOPGLOBAL"]
EXCHANGEPALABRASUNICAS = os.environ["EXCHANGEPALABRASUNICAS"]
TOTALSUMTOP = int(os.environ["TOTALSUMTOP"])
TOTALTOPGLOBAL = int(os.environ["TOTALTOPGLOBAL"])
TOTALPALABRASUNICAS = int(os.environ["TOTALPALABRASUNICAS"])
TOP_SIZE=20
ID = os.environ["ID"]


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
            self.clientes[mensaje.clienteId] = [0, {}]
        if mensaje.language not in self.clientes[mensaje.clienteId][1]:
            self.clientes[mensaje.clienteId][1][mensaje.lenguaje] = {}
            
        for clave, valor in mensaje.palabras.items():
            self.clientes[mensaje.clienteId][1][mensaje.lenguaje][clave] = self.clientes[mensaje.clienteId][1][mensaje.lenguaje].get(clave, 0) + valor
        
    def _top20(self, palabras: dict[str, int]) -> dict[str, int]:
        top = sorted(palabras.items(), key=lambda item: item[1], reverse=True)
        return dict(top[:TOP_SIZE])

    def _procesarEOF(self, mensaje: FinMensajeSistema) -> None:
        self.clientes[mensaje.clienteId][0] += 1
        if self.clientes[mensaje.clienteId][0] == TOTALSUMTOP:
            
            print(self._top20(self.clientes[mensaje.clienteId][1]))

            duplicadas = []
            lenguajes = self.clientes[mensaje.clienteId][1].keys()
            mergedTop = self.clientes[mensaje.clienteId][1][lenguajes[0]]
            for palabra, cuenta in self.clientes[mensaje.clienteId][1][lenguajes[1]].items():
                if palabra in mergedTop:
                    mergedTop[palabra] += cuenta
                    duplicadas.append(palabra) # TODO: Puede encolarse en respuestas tipo streaming 
                else:
                    mergedTop[palabra] = cuenta                
            self.colaRespuestas.send(Respuesta3MensajeSistema(clienteId=mensaje.clienteId, palabras=duplicadas))
                
            nodo = mensaje.clienteId.int % TOTALTOPGLOBAL
            self.exchangeTopGlobal[nodo].send(PalabrasMensajeSistema(clienteId=mensaje.clienteId, palabras=self._top20(mergedTop), url="", lenguaje=0).aBytes())    
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
            print(e)
            print(traceback.format_exc())
            nack()

    def iniciar(self):
        self.exchangeTopParcial.start_consuming(self.procesarMensaje)


    def manejarSigterm(self) -> None:
        pass


def main() -> int:
    agregadorTop = AgregadorTop()
    signal.signal(signal.SIGTERM, lambda signum, frame: agregadorTop.manejarSigterm())
    agregadorTop.iniciar()
    return 0


if __name__ == "__main__":
    main()