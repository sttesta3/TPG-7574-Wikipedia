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
        self.threadControl = threading.Thread(target=lambda: asyncio.run(self.controlar()), daemon=True)
        self.threadControl.start()


    async def reiniciarServicio(self, servicio):
        print(f"reinicio {servicio}")
        subprocess.run(["docker", "restart", servicio], check=True)
        conectado = False
        while not conectado:
            try:
                reader, writer = await asyncio.open_connection(servicio, MAESTROPORT)
                conectado = True
            except Exception as e:
                asyncio.sleep(1)

        self.nodos[servicio].setearMedio(lambda: self.pedirLatido(servicio, writer, reader))
        

    async def pedirLatido(self, servicio, writer, reader):
        try:
            self.nodos[servicio].setearLargo(lambda: self.reiniciarServicio(servicio))
            writer.write(LATIDO_MENSAJE)
            await writer.drain() 

            self.nodos[servicio].setearLargo(lambda: self.reiniciarServicio(servicio))


            await reader.readexactly(1)
            print(f"Latio {servicio}")
            self.nodos[servicio].setearMedio(lambda: self.pedirLatido(servicio, writer, reader))

        except Exception:
            return

    async def controlar(self):
        print("soy lider")
        for servicio in SERVICIOS.split(","):
            try:
                reader, writer = await asyncio.open_connection(servicio, MAESTROPORT)
                self.nodos[servicio] = Timer()
                print(f"me conecto a {servicio}")
                asyncio.create_task(self.pedirLatido(servicio, writer, reader))
            except Exception as e:
                logging.info(e)
                asyncio.create_task(self.reiniciarServicio(servicio))
        
        await asyncio.Event().wait()

    def manejarSigterm(self) -> None:
        # TODO: hay q matar todo lo que queda dando vueltas
        pass


def main() -> int:
    logging.basicConfig(level=logging.INFO)
    maestro = Maestro()
    signal.signal(signal.SIGTERM, lambda signum, frame: maestro.manejarSigterm())
    maestro.iniciar()
    return 0


if __name__ == "__main__":
    main()
