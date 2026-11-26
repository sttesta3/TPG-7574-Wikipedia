import asyncio
import random

class Timer():
    def __init__(self) -> None:
        self.loop = asyncio.get_running_loop()
        self.timer = None

    
    def _setear(self, min, max, fn):
        if self.timer is not None:
            self.timer.cancel()

        self.timer = self.loop.call_later(random.randint(min, max) / 1000,  lambda: asyncio.create_task(fn()))
    

    def setearLargo(self, fn):
        self._setear(500, 1000, fn)


    def setearMedio(self, fn):
        self._setear(150, 250, fn)
        

    def setearCorto(self, fn):
        self._setear(50, 100, fn)


    def cancelar(self):
        if self.timer is not None:
            self.timer.cancel()
        self.timer = None