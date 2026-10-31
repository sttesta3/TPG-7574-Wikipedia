import os
import signal
import traceback
from middleware import MessageMiddlewareExchange
from mensajesSistema import recvMensajeSistema, FinMensajeSistema, PalabrasMensajeSistema


MOMHOST = os.environ["MOMHOST"]
COLASUMTOP = os.environ["COLASUMTOP"]
EXCHANGETOPPARCIAL = os.environ["EXCHANGETOPPARCIAL"]
EXCHANGETOPGLOBAL = os.environ["EXCHANGETOPGLOBAL"]
TOTALSUMTOP = int(os.environ["TOTALSUMTOP"])
TOTALTOPGLOBAL = int(os.environ["TOTALTOPGLOBAL"])
ID = os.environ["ID"]


class AgregadorTop:
    def __init__(self):
        self.exchangeTopParcial = MessageMiddlewareExchange(MOMHOST, EXCHANGETOPPARCIAL, [EXCHANGETOPPARCIAL+"_"+str(ID)])
        self.exchangeTopGlobal = []
        for i in range(TOTALTOPGLOBAL):
            self.exchangeTopGlobal.append(MessageMiddlewareExchange(MOMHOST, EXCHANGETOPGLOBAL, [EXCHANGETOPGLOBAL+"_"+str(i)]))
         
        self.clientes = {}


    def _procesarData(self, mensaje: PalabrasMensajeSistema) -> None:
        if mensaje.clienteId not in self.clientes:
            self.clientes[mensaje.clienteId] = [0, {}]

        for clave, valor in mensaje.palabras.items():
            self.clientes[mensaje.clienteId][1][clave] = self.clientes[mensaje.clienteId][1].get(clave, 0) + valor


    def _top20(self, palabras: dict[str, int]) -> dict[str, int]:
        top = sorted(palabras.items(), key=lambda item: item[1], reverse=True)
        return dict(top[:20])

    def _procesarEOF(self, mensaje: FinMensajeSistema) -> None:
        self.clientes[mensaje.clienteId][0] += 1
        if self.clientes[mensaje.clienteId][0] == TOTALSUMTOP:
            nodo = mensaje.clienteId.int % TOTALTOPGLOBAL
            self.exchangeTopGlobal[nodo].send(PalabrasMensajeSistema(clienteId=mensaje.clienteId, palabras=self._top20(self.clientes[mensaje.clienteId][1]), url="", lenguaje=0).aBytes())    
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
        self._close_connections()


    def manejarSigterm(self) -> None:
        self.exchangeTopParcial.remote_stop()


    def _close_connections(self):
        self.exchangeTopParcial.close()
        for i in range(TOTALTOPGLOBAL):
            self.exchangeTopGlobal[i].close()


def main() -> int:
    agregadorTop = AgregadorTop()
    signal.signal(signal.SIGTERM, lambda signum, frame: agregadorTop.manejarSigterm())
    agregadorTop.iniciar()
    return 0


if __name__ == "__main__":
    main()