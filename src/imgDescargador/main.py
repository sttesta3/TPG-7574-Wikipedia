import os
import sys
import logging
import signal
import aiohttp
import asyncio
import traceback
import threading
from clienteLock import ClienteLock
from protocolo.mensajesSistema import recvMensajeSistema, FinMensajeSistema, ImgMensajeSistema, Respuesta2MensajeSistema
from middleware import MessageMiddlewareQueue, MessageMiddlewareExchange

MOMHOST = os.environ["MOMHOST"]
COLAIMGDESCARGA = os.environ["COLAIMGDESCARGA"]
COLARESPUESTAS = os.environ["COLARESPUESTAS"]
EXCHANGEIMGEOF = os.environ["EXCHANGEIMGEOF"]
TOTALCLASIFICADORES = int(os.environ["TOTALCLASIFICADORES"])
MAXCLIENTES = int(os.environ["MAXCLIENTES"])

class ImgDescargador:
    def __init__(self):
        self.eventLoop = asyncio.new_event_loop()
        self.clientes = {}
        self.lock = threading.Lock()
        self.maxClientes = 0

        self.colaImgDescarga = MessageMiddlewareQueue(MOMHOST, COLAIMGDESCARGA)
        self.colaRespuestas = MessageMiddlewareQueue(MOMHOST, COLARESPUESTAS)
        self.exchangeImgEof = MessageMiddlewareExchange(MOMHOST, EXCHANGEIMGEOF, [EXCHANGEIMGEOF])
        self.exchangeImgEofSend = MessageMiddlewareExchange(MOMHOST, EXCHANGEIMGEOF, [EXCHANGEIMGEOF])


    async def _procesarData(self, mensaje: ImgMensajeSistema, eof: bool = False ) -> None:
        if eof:
            self.colaRespuestas.send(FinMensajeSistema(mensaje.clienteId).aBytes())
            del self.clientes[mensaje.clienteId]
            return 
        
        try:
            imgBytes = b''
            if mensaje.imgUrl != "":
                # TODO: podria manejar una sola sesion como variable del ImgDescargador
                async with aiohttp.ClientSession(headers={'User-Agent':'Tp-Fiuba/0.0 (https://fi.uba.ar/;shenseler@fi.uba.ar)'}) as session:
                    async with session.get(mensaje.imgUrl) as resp:
                        if resp.status == 200:
                            imgBytes = await resp.read()

            self.colaRespuestas.send(Respuesta2MensajeSistema(mensaje.clienteId, mensaje.url, mensaje.nombre, imgBytes).aBytes())
        finally:
            # Corre tambien si la descarga falla o se cancela, para no dejar bloqueado al hilo de EOF
            self.clientes[mensaje.clienteId].nuevaRespuesta()
            with self.lock:
                self.maxClientes -= 1


    async def _cancelarDescargas(self) -> None:
        actual = asyncio.current_task()
        pendientes = [tarea for tarea in asyncio.all_tasks() if tarea is not actual]
        for tarea in pendientes:
            tarea.cancel()
        await asyncio.gather(*pendientes, return_exceptions=True)


    def _procesarEOF(self, mensaje: FinMensajeSistema) -> None:
        self.exchangeImgEofSend.send(mensaje.aBytes())
        

    def procesarMensaje(self, bytes, ack, nack):
        try:
            mensaje = recvMensajeSistema(bytes)
            if isinstance(mensaje, FinMensajeSistema): # TODO: esta bien esto?
                self._procesarEOF(mensaje)
            else:
                if mensaje.clienteId not in self.clientes:
                    self.clientes[mensaje.clienteId] = ClienteLock(TOTALCLASIFICADORES)

                self.clientes[mensaje.clienteId].nuevoMensaje()
                asyncio.run_coroutine_threadsafe(self._procesarData(mensaje), self.eventLoop)
            ack()
        except Exception as e:
            logging.info(e)
            ack()


    def _controlarEof(self):
        
        def manejarEof(bytes, ack, nack):
            with self.lock:
                if self.maxClientes < MAXCLIENTES:
                    self.maxClientes += 1
                else:
                    nack()
                    return

            try:
                mensaje = recvMensajeSistema(bytes)
                if mensaje.clienteId not in self.clientes:
                    self.clientes[mensaje.clienteId] = ClienteLock()

                if self.clientes[mensaje.clienteId].llegadaEof():
                    asyncio.run_coroutine_threadsafe(self._procesarData(ImgMensajeSistema(mensaje.clienteId), True), self.eventLoop)
                
                ack()
            except Exception as e:
                logging.info(e)
                logging.info(traceback.format_exc())
                nack()

        self.exchangeImgEof.start_consuming(manejarEof)


    def _iniciarEventLoop(self):
        asyncio.set_event_loop(self.eventLoop)
        self.eventLoop.run_forever()


    def iniciar(self):
        thread_event_loop = threading.Thread(target=self._iniciarEventLoop, daemon=True)

        thread_eof = threading.Thread(target=self._controlarEof, daemon=True)

        thread_event_loop.start()
        thread_eof.start()
        self.colaImgDescarga.start_consuming(self.procesarMensaje)

        # Primero se cancelan las descargas: el hilo de EOF puede estar esperandolas en cond.wait()
        asyncio.run_coroutine_threadsafe(self._cancelarDescargas(), self.eventLoop).result(timeout=5)
        thread_eof.join()
        self.eventLoop.call_soon_threadsafe(self.eventLoop.stop)
        thread_event_loop.join()
        self.eventLoop.close()
        self._close_connections()


    def manejarSigterm(self) -> None:
        self.colaImgDescarga.remote_stop()
        self.exchangeImgEof.remote_stop()


    def _close_connections(self):
        self.colaImgDescarga.close()
        self.colaRespuestas.close()
        self.exchangeImgEof.close()
        self.exchangeImgEofSend.close()


def main() -> int:
    logging.basicConfig(level=logging.INFO)
    imgDescargador = ImgDescargador()
    signal.signal(signal.SIGTERM, lambda signum, frame: imgDescargador.manejarSigterm())
    imgDescargador.iniciar()
    return 0


if __name__ == "__main__":
    main()
