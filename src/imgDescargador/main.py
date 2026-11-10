import os
import sys
import logging
import signal
import random
import email.utils
from datetime import datetime, timezone
import aiohttp
import asyncio
import traceback
import threading
from contadorDistribuido import contadorDistribuido
from protocolo.mensajesSistema import recvMensajeSistema, FinMensajeSistema, ImgMensajeSistema, ImgLoteMensajeSistema, Respuesta2MensajeSistema
from middleware import MessageMiddlewareQueue

MOMHOST = os.environ["MOMHOST"]
COLAIMGDESCARGA = os.environ["COLAIMGDESCARGA"]
COLARESPUESTAS = os.environ["COLARESPUESTAS"]
EXCHANGEIMGEOF = os.environ["EXCHANGEIMGEOF"]
MAXCLIENTES = int(os.environ["MAXCLIENTES"])
DESCARGASPORMINUTO = float(os.environ["DESCARGASPORMINUTO"])
USER_AGENT = f"TpFiubaWikiBot/0.1 (https://fi.uba.ar/; shenseler@fi.uba.ar) aiohttp/{aiohttp.__version__}"
REINTENTOS_DESCARGA = 4
BACKOFF_BASE = 5
ESPERA_MAXIMA = 60
TIMEOUT_DESCARGA = 30


class DescargaReintentable(Exception):
    def __init__(self, motivo: str, retryAfter: float = 0) -> None:
        super().__init__(motivo)
        self.retryAfter = retryAfter


def leerRetryAfter(valor: str | None) -> float:
    if valor is None:
        return 0
    try:
        return max(0.0, float(valor))
    except ValueError:
        pass
    try:
        fecha = email.utils.parsedate_to_datetime(valor)
        return max(0.0, (fecha - datetime.now(timezone.utc)).total_seconds())
    except (TypeError, ValueError):
        return 0


class ImgDescargador:
    def __init__(self):
        self.eventLoop = asyncio.new_event_loop()
        self.descargasSimultaneas = asyncio.Semaphore(MAXCLIENTES)
        self.intervaloEntrePedidos = 60 / DESCARGASPORMINUTO
        self.turnoPedidos = asyncio.Lock()
        self.proximoPedido = 0.0

        self.colaImgDescarga = MessageMiddlewareQueue(MOMHOST, COLAIMGDESCARGA)
        self.colaRespuestas = MessageMiddlewareQueue(MOMHOST, COLARESPUESTAS)

        self.contador = contadorDistribuido(MOMHOST, EXCHANGEIMGEOF, self._finalizarCliente, self.colaImgDescarga.remote_execution)


    async def _esperarTurno(self) -> None:
        async with self.turnoPedidos:
            loop = asyncio.get_running_loop()
            espera = self.proximoPedido - loop.time()
            if espera > 0:
                await asyncio.sleep(espera)
            self.proximoPedido = loop.time() + self.intervaloEntrePedidos


    async def _intentarDescarga(self, imgUrl: str) -> bytes:
        await self._esperarTurno()
        async with self.descargasSimultaneas:
            async with aiohttp.ClientSession(headers={'User-Agent': USER_AGENT}, timeout=aiohttp.ClientTimeout(total=TIMEOUT_DESCARGA)) as session:
                async with session.get(imgUrl) as resp:
                    if resp.status == 200:
                        return await resp.read()
                    if resp.status == 429 or resp.status >= 500:
                        raise DescargaReintentable(f"status {resp.status}", leerRetryAfter(resp.headers.get("Retry-After")))
                    return b''


    async def _descargarConReintentos(self, mensaje: ImgMensajeSistema) -> bytes:
        for intento in range(REINTENTOS_DESCARGA + 1):
            try:
                return await self._intentarDescarga(mensaje.imgUrl)
            except (aiohttp.ClientError, asyncio.TimeoutError, DescargaReintentable) as e:
                if intento == REINTENTOS_DESCARGA:
                    logging.warning(f"Descarga de {mensaje.imgUrl} fallo {intento + 1} veces, la mando sin imagen: {e!r}")
                    return b''
                retryAfter = e.retryAfter if isinstance(e, DescargaReintentable) else 0
                espera = min(max(retryAfter, BACKOFF_BASE * (2 ** intento)) * random.uniform(1, 1.2), ESPERA_MAXIMA)
                logging.info(f"Reintento {intento + 1} de {mensaje.imgUrl} en {espera:.2f}s (Retry-After={retryAfter}): {e!r}")
                await asyncio.sleep(espera)


    async def _descargar(self, mensaje: ImgMensajeSistema) -> None:
        imgBytes = b''
        if mensaje.imgUrl != "":
            imgBytes = await self._descargarConReintentos(mensaje)

        self.colaRespuestas.send(Respuesta2MensajeSistema(mensaje.clienteId, mensaje.url, mensaje.nombre, imgBytes).aBytes())


    async def _procesarLote(self, lote: ImgLoteMensajeSistema) -> None:
        clienteId = lote.clienteId
        secuencia = lote.secuencia

        resultados = await asyncio.gather(*[self._descargar(mensaje) for mensaje in lote.mensajes], return_exceptions=True)
        for resultado in resultados:
            if isinstance(resultado, Exception):
                logging.info(f"Fallo una descarga del lote {secuencia} de {clienteId}: {resultado}")

        self.colaImgDescarga.remote_execution(lambda: self.contador.procesado(clienteId, secuencia))


    def _enviarFin(self, clienteId) -> None:
        self.colaRespuestas.send(FinMensajeSistema(clienteId).aBytes())
        logging.info(f"Mando EOF de {clienteId}")


    def _finalizarCliente(self, clienteId, fin: FinMensajeSistema, originador: bool) -> None:
        self.eventLoop.call_soon_threadsafe(lambda: self._enviarFin(clienteId))


    async def _cancelarDescargas(self) -> None:
        actual = asyncio.current_task()
        pendientes = [tarea for tarea in asyncio.all_tasks() if tarea is not actual]
        for tarea in pendientes:
            tarea.cancel()
        await asyncio.gather(*pendientes, return_exceptions=True)


    def procesarMensaje(self, bytes, ack, nack):
        try:
            mensaje = recvMensajeSistema(bytes)
            if isinstance(mensaje, FinMensajeSistema):
                self.contador.eofRecibido(mensaje)
            elif self.contador.yaFinalizado(mensaje.clienteId):
                logging.info(f"Descarto lote {mensaje.secuencia} de {mensaje.clienteId}: cliente ya finalizado")
            else:
                asyncio.run_coroutine_threadsafe(self._procesarLote(mensaje), self.eventLoop)
            ack()
        except Exception as e:
            logging.info(e)
            logging.info(traceback.format_exc())
            nack()


    def _iniciarEventLoop(self):
        asyncio.set_event_loop(self.eventLoop)
        self.eventLoop.run_forever()


    def iniciar(self):
        thread_event_loop = threading.Thread(target=self._iniciarEventLoop, daemon=True)
        thread_contador = threading.Thread(target=self.contador.iniciar, daemon=True)

        thread_event_loop.start()
        thread_contador.start()
        self.colaImgDescarga.start_consuming(self.procesarMensaje)

        asyncio.run_coroutine_threadsafe(self._cancelarDescargas(), self.eventLoop).result(timeout=5)
        thread_contador.join()
        self.eventLoop.call_soon_threadsafe(self.eventLoop.stop)
        thread_event_loop.join()
        self.eventLoop.close()
        self._close_connections()


    def manejarSigterm(self) -> None:
        self.contador.detener()
        self.colaImgDescarga.remote_stop()


    def _close_connections(self):
        self.colaImgDescarga.close()
        self.colaRespuestas.close()
        self.contador.cerrar()


def main() -> int:
    logging.basicConfig(level=logging.INFO)
    imgDescargador = ImgDescargador()
    signal.signal(signal.SIGTERM, lambda signum, frame: imgDescargador.manejarSigterm())
    imgDescargador.iniciar()
    return 0


if __name__ == "__main__":
    main()
