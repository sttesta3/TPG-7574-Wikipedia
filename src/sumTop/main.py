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

class ClienteLock():
    def __init__(self) -> None:
        self.cond = threading.Condition()
        self.eof = 0
        self.respuestas = 0


    def nuevoMensaje(self) -> None:
        with self.cond:
            self.respuestas += 1


    def nuevaRespuesta(self):
        with self.cond:
            self.respuestas -= 1
            if self.respuestas <= 0 and self.eof == 3:
                self.cond.notify_all()
            

    def llegadaEof(self) -> bool:
        llego = False
        with self.cond:
            self.eof += 1
            if self.eof == 2:
                while self.respuestas > 0:
                    self.cond.wait()
                llego = True
        return llego


class SumTop:
    def __init__(self):
        self.colaSumTop = MessageMiddlewareQueue(MOMHOST, COLASUMTOP)
        self.exchangeSumTopEofSend = MessageMiddlewareExchange(MOMHOST, EXCHANGESUMTOPEOF, [EXCHANGESUMTOPEOF])
        self.exchangeSumTopEof = MessageMiddlewareExchange(MOMHOST, EXCHANGESUMTOPEOF, [EXCHANGESUMTOPEOF])
        self.excahangeTopParciales = []
        for i in range(TOTALTOPPARCIAL):
            self.excahangeTopParciales.append(MessageMiddlewareExchange(MOMHOST, EXCHANGETOPPARCIAL, [EXCHANGETOPPARCIAL+ "_"+str(i)]))

        self.clientes = {}
        self.clientesLock = {}


    def _procesarData(self, mensaje: PalabrasMensajeSistema) -> None:      
        if mensaje.clienteId not in self.clientes:
            self.clientes[mensaje.clienteId] = {}
            self.clientesLock[mensaje.clienteId] = ClienteLock()

        self.clientesLock[mensaje.clienteId].nuevoMensaje()

        for clave, valor in mensaje.palabras.items():
            self.clientes[mensaje.clienteId][clave] = self.clientes[mensaje.clienteId].get(clave, 0) + valor

        self.clientesLock[mensaje.clienteId].nuevaRespuesta()


    def _procesarEOF(self, mensaje: FinMensajeSistema) -> None:
        self.exchangeSumTopEofSend.send(mensaje.aBytes())


    def procesarMensaje(self, bytes, ack, nack):
        try:
            mensaje = recvMensajeSistema(bytes)
            if isinstance(mensaje, FinMensajeSistema): # TODO: esta bien esto?
                self._procesarEOF(mensaje)
            else:
                print("ms")
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
            if self.clientesLock[mensaje.clienteId].llegadaEof():
                print("ENVIO EOF")
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