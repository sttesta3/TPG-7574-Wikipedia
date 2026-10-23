import os
import sys
import signal
import threading
import aiohttp
import asyncio
import traceback
from mensajesSistema import recvMensajeSistema, FinMensajeSistema, ImgMensajeSistema, Respuesta2MensajeSistema
from middleware import MessageMiddlewareQueue, MessageMiddlewareExchange

MOMHOST = os.environ["MOMHOST"]
COLAIMGDESCARGA = os.environ["COLAIMGDESCARGA"]
COLARESPUESTAS = os.environ["COLARESPUESTAS"]
EXCHANGEIMGEOF = os.environ["EXCHANGEIMGEOF"]

class ClienteLock():
    def __init__(self) -> None:
        self.lock = threading.Lock()
        self.eof = False
        self.respuestas = 0


    def nuevoMensaje(self) -> None:
        with self.lock:
            self.respuestas += 1


    def nuevaRespuesta(self) -> bool:
        rta = False
        with self.lock:
            self.respuestas -= 1
            if self.respuestas <= 0 and self.eof:
                rta = True
        return rta
    

    def llegadaEof(self) -> bool:
        rta = False
        with self.lock:
            self.eof = True
            if self.respuestas <= 0:
                rta = True
        return rta
            

class ImgDescargador:
    def __init__(self):
        self.eventLoop = asyncio.new_event_loop()
        self.clientes = {}

        self.colaImgDescarga = MessageMiddlewareQueue(MOMHOST, COLAIMGDESCARGA)
        self.colaRespuestas = MessageMiddlewareQueue(MOMHOST, COLARESPUESTAS)
        self.exchangeImgEof = MessageMiddlewareExchange(MOMHOST, EXCHANGEIMGEOF, [EXCHANGEIMGEOF])
        self.exchangeImgEofSend = MessageMiddlewareExchange(MOMHOST, EXCHANGEIMGEOF, [EXCHANGEIMGEOF])


    async def _procesarData(self, mensaje: ImgMensajeSistema) -> None:
        if mensaje.nombre is not None:
            imgBytes = b''
            if mensaje.url != "":
                async with aiohttp.ClientSession() as session:
                    async with session.get(mensaje.url) as resp:
                        #print(await resp.read())
                        imgBytes = await resp.read()

            self.colaRespuestas.send(Respuesta2MensajeSistema(mensaje.clienteId, mensaje.url, mensaje.nombre, imgBytes).aBytes())

        if self.clientes[mensaje.clienteId].nuevaRespuesta():
            self.colaRespuestas.send(FinMensajeSistema(mensaje.clienteId).aBytes())
            del self.clientes[mensaje.clienteId]


    def _procesarEOF(self, mensaje: FinMensajeSistema) -> None:
        self.exchangeImgEofSend.send(mensaje.aBytes())
        

    def procesarMensaje(self, bytes, ack, nack):
        try:
            mensaje = recvMensajeSistema(bytes)
            if isinstance(mensaje, FinMensajeSistema): # TODO: esta bien esto?
                self._procesarEOF(mensaje)
            else:
                if mensaje.clienteId not in self.clientes:
                    self.clientes[mensaje.clienteId] = ClienteLock()
                
                self.clientes[mensaje.clienteId].nuevoMensaje()
                asyncio.run_coroutine_threadsafe(self._procesarData(mensaje), self.eventLoop)
            ack()
        except Exception as e:
            print(e)
            ack()


    def _controlarEof(self):
        
        def manejarEof(bytes, ack, nack):
            try:
                mensaje = recvMensajeSistema(bytes)

                if mensaje.clienteId not in self.clientes:
                    self.clientes[mensaje.clienteId] = ClienteLock()

                if self.clientes[mensaje.clienteId].llegadaEof():
                    asyncio.run_coroutine_threadsafe(self._procesarData(ImgMensajeSistema(mensaje.clienteId)), self.eventLoop)
                ack()
            except Exception as e:
                print(e)
                print(traceback.format_exc())
                nack()

        self.exchangeImgEof.start_consuming(manejarEof)


    def _iniciarEventLoop(self):
        asyncio.set_event_loop(self.eventLoop)
        self.eventLoop.run_forever()


    def iniciar(self):
        threading.Thread(target=self._iniciarEventLoop, daemon=True).start()
        threading.Thread(target=self._controlarEof, daemon=True).start()
        self.colaImgDescarga.start_consuming(self.procesarMensaje)


    def manejarSigterm(self) -> None:
        pass


def main() -> int:
    imgDescargador = ImgDescargador()
    signal.signal(signal.SIGTERM, lambda signum, frame: imgDescargador.manejarSigterm())
    imgDescargador.iniciar()
    return 0


if __name__ == "__main__":
    main()