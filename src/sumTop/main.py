import os
import sys
import signal
import threading
from mensajesSistema import recvMensajeSistema, FinMensajeSistema, TransformadorMensajeSistema, PalabrasMensajeSistema, CantidadPalabraMensajeSistema
from middleware import MessageMiddlewareQueue, MessageMiddlewareExchange

import traceback

MOMHOST = os.environ["MOMHOST"]
COLASUMTOP = os.environ["COLASUMTOP"]
EXCHANGESUMTOPEOF = os.environ["EXCHANGESUMTOPEOF"]
EXCHANGETOPPARCIAL = os.environ["EXCHANGETOPPARCIAL"]
TOTALTOPPARCIAL = int(os.environ["TOTALTOPPARCIAL"])


class SumTop:
    def __init__(self):
        self.colaSumTop = MessageMiddlewareQueue(MOMHOST, COLASUMTOP)
        self.exchangeSumTopEofSend = MessageMiddlewareExchange(MOMHOST, EXCHANGESUMTOPEOF, [EXCHANGESUMTOPEOF])
        self.exchangeSumTopEof = MessageMiddlewareExchange(MOMHOST, EXCHANGESUMTOPEOF, [EXCHANGESUMTOPEOF])
        self.excahangeTopParciales = []
        for i in range(TOTALTOPPARCIAL):
            self.excahangeTopParciales.append(MessageMiddlewareExchange(MOMHOST, EXCHANGETOPPARCIAL, [EXCHANGETOPPARCIAL+ "_"+str(i)]))

        self.clientes = {}
        self.a = 0
        self.lock = threading.Lock()


    def _procesarData(self, mensaje: PalabrasMensajeSistema) -> None:
        with self.lock:
            if mensaje.clienteId not in self.clientes:
                self.clientes[mensaje.clienteId] = {}

            for clave, valor in mensaje.palabras.items():
                if clave == "découvert":
                    self.a += 1
                self.clientes[mensaje.clienteId][clave] = self.clientes[mensaje.clienteId].get(clave, 0) + valor


    def _procesarEOF(self, mensaje: FinMensajeSistema) -> None:
        print("LLEGO EOF")
        print(f"aca {self.a}")
        self.exchangeSumTopEofSend.send(mensaje.aBytes())


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


    def _top20(self, palabras: dict[str, int]) -> dict[str, int]:
        top = sorted(palabras.items(), key=lambda item: item[1], reverse=True)
        return dict(top[:20])


    def _manejarEof(self, bytes, ack, nack):
        try:
            mensaje = recvMensajeSistema(bytes)
            with self.lock:
                print(f"acacve{self.a}")
                nodos = [{} for _ in range(TOTALTOPPARCIAL)]
                for clave, valor in self.clientes[mensaje.clienteId].items():
                    i = int.from_bytes(clave.encode("UTF-8")) % TOTALTOPPARCIAL
                    nodos[i][clave] = valor

                for i in range(TOTALTOPPARCIAL):
                    print(f"MANDO: {self._top20(nodos[i])}")
                    mensaje = PalabrasMensajeSistema(palabras=nodos[i], clienteId=mensaje.clienteId, url="", lenguaje=0)
                    self.excahangeTopParciales[i].send(mensaje.aBytes())
                    self.excahangeTopParciales[i].send(FinMensajeSistema(mensaje.clienteId).aBytes())

                
            ack()
        except Exception as e:
            print(e)
            nack()
    
    
    def _controlarEof(self):
        self.exchangeSumTopEof.start_consuming(self._manejarEof)


    def iniciar(self):
        threading.Thread(target=self._controlarEof, daemon=True).start()
        self.colaSumTop.start_consuming(self.procesarMensaje)


    def manejarSigterm(self) -> None:
        pass


def main() -> int:
    sumTop = SumTop()
    signal.signal(signal.SIGTERM, lambda signum, frame: sumTop.manejarSigterm())
    sumTop.iniciar()
    return 0


if __name__ == "__main__":
    main()