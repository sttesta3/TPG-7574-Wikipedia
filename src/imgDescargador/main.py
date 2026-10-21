import os
import sys
import signal
import threading
import aiohttp
import asyncio
from mensajesSistema import recvMensajeSistema, FinMensajeSistema, ImgMensajeSistema, Respuesta2MensajeSistema
from middleware import MessageMiddlewareQueue

MOMHOST = os.environ["MOMHOST"]
COLAIMGDESCARGA = os.environ["COLAIMGDESCARGA"]
COLARESPUESTAS = os.environ["COLARESPUESTAS"]

class ImgDescargador:
    def __init__(self):
        self.eventLoop = asyncio.new_event_loop()
        self.lock = threading.Lock()
        threading.Thread(target=self._iniciarEventLoop, daemon=True).start()

        self.colaImgDescarga = MessageMiddlewareQueue(MOMHOST, COLAIMGDESCARGA)
        self.colaRespuestas = MessageMiddlewareQueue(MOMHOST, COLARESPUESTAS)


    def _iniciarEventLoop(self):
        asyncio.set_event_loop(self.eventLoop)
        self.eventLoop.run_forever()


    async def _procesarData(self, mensaje: ImgMensajeSistema) -> None:
        imgBytes = b''
        if mensaje.url != "":
            async with aiohttp.ClientSession() as session:
                async with session.get(mensaje.url) as resp:
                    print(await resp.read())
                    imgBytes = await resp.read()

        self.colaRespuestas.send(Respuesta2MensajeSistema(mensaje.clienteId, mensaje.url, mensaje.nombre, imgBytes).aBytes())


    def _procesarEOF(self, mensaje: FinMensajeSistema) -> None:
        print(f"Llego EOF {mensaje.clienteId}")
        #TODO: que hago con esto (?
        

    def procesarMensaje(self, bytes, ack, nack):
        try:
            mensaje = recvMensajeSistema(bytes)
            if isinstance(mensaje, FinMensajeSistema): # TODO: esta bien esto?
                self._procesarEOF(mensaje)
            else:
                asyncio.run_coroutine_threadsafe(self._procesarData(mensaje), self.eventLoop)
            ack()
        except Exception as e:
            print(e)
            nack()


    def iniciar(self):
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