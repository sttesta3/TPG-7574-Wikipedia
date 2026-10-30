import threading

class ClienteLock():
    def __init__(self, totalEof: int = 1) -> None:
        self.cond = threading.Condition()
        self.eof = 0
        self.respuestas = 0
        self.totalEof = totalEof


    def nuevoMensaje(self) -> None:
        with self.cond:
            self.respuestas += 1


    def nuevaRespuesta(self):
        with self.cond:
            self.respuestas -= 1
            if self.respuestas <= 0 and self.eof == self.totalEof:
                self.cond.notify_all()
            

    def llegadaEof(self) -> bool:
        llego = False
        with self.cond:
            self.eof += 1
            if self.eof == self.totalEof:
                while self.respuestas > 0:
                    self.cond.wait()
                llego = True
        return llego