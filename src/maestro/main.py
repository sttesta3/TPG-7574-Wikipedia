import os
import signal
import asyncio
import logging
import threading
import subprocess
from raft import Raft
from timer import Timer

MAESTROPORT = int(os.environ["MAESTROPORT"])
SERVICIOS = os.environ["SERVICIOS"]

LECTURA = 0
ESCRITURA = 1

LATIDO_MENSAJE = b'\x01'

class Maestro:
    def __init__(self):
        self.raft = Raft()
        self.threadControl = None

        self.nodos = {}


    def iniciar(self):
        self.raft.iniciarRaft(self.iniciarControl)


    def iniciarControl(self):
        self.threadControl = threading.Thread(target=self.controlar, daemon=True)


    async def reiniciarServicio(self, servicio):
        subprocess.run(["docker", "restart", servicio], check=True)

        reader, writer = await asyncio.open_connection(servicio, MAESTROPORT)

        self.nodos[servicio].setearMedio(lambda: self.pedirLatido(servicio, writer, reader))
        

    async def pedirLatido(self, servicio, writer, reader):
        writer.write(LATIDO_MENSAJE)
        await writer.drain() 

        self.nodos[servicio].setearLargo(lambda: self.reiniciarServicio(servicio))

        await reader.readexactly(1)

        self.nodos[servicio].setearMedio(lambda: self.pedirLatido(servicio, writer, reader))
        

    async def controlar(self):
        for servicio in SERVICIOS.split(","):
            try:
                reader, writer = await asyncio.open_connection(servicio, MAESTROPORT)
                self.nodos[servicio] = Timer()
                asyncio.create_task(self.pedirLatido(servicio, writer, reader))
            except Exception:
                asyncio.create_task(self.reiniciarServicio(servicio))
            

    def manejarSigterm(self) -> None:
        pass


def main() -> int:
    logging.basicConfig(level=logging.INFO)
    maestro = Maestro()
    signal.signal(signal.SIGTERM, lambda signum, frame: maestro.manejarSigterm())
    maestro.iniciar()
    return 0


if __name__ == "__main__":
    main()
