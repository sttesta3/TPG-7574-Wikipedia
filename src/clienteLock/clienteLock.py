import threading

class ClienteLock():
    def __init__(self) -> None:
        self.cond = threading.Lock()
        self.respuestas = 0

    def nuevoMensaje(self, cant: int = 1) -> None:
        with self.cond:
            self.respuestas += cant

    def cantMensajes(self) -> int:
        result = 0
        with self.cond:
            result = self.respuestas
        return result 
