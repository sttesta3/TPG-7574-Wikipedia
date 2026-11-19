import signal
import logging
import threading
from raft import Raft

class Maestro:
    def __init__(self):
        self.raft = Raft()

    
    def iniciar(self):
        raft = threading.Thread(target=self.raft.iniciarRaft, daemon=True)
        raft.start()
        raft.join()

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
