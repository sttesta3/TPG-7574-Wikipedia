import os
from mensajesSistema import recvMensajeSistema, FinMensajeSistema, CantidadPalabraMensajeSistema, FinPromMensajeSistema
from middleware import MessageMiddlewareExchange

MOMHOST = os.environ["MOMHOST"]
EXCHANGEPROMEDIO = os.environ["EXCHANGEPROMEDIO"]
EXCHANGECUENTAPROM = os.environ["EXCHANGECUENTAPROM"]
TOTALCUENTAPROM = int(os.environ["TOTALCUENTAPROM"])
ID = os.environ["ID"]


class Promedio:
    def __init__(self):
        self.clientes = {}
        self.exchangePromedio = MessageMiddlewareExchange(MOMHOST, EXCHANGEPROMEDIO, [EXCHANGEPROMEDIO + "_" + ID])
        self.exchangeCuentaProm = []
        for i in range(TOTALCUENTAPROM):
            self.exchangeCuentaProm.append(MessageMiddlewareExchange(MOMHOST, EXCHANGECUENTAPROM, [EXCHANGECUENTAPROM + "_" + str(i)]))


    def _procesarData(self, mensaje: CantidadPalabraMensajeSistema) -> None:
        clienteId = str(mensaje.clienteId)
        if clienteId not in self.clientes:
            self.clientes[clienteId] = [mensaje.cantidad, 1]
        else:
            self.clientes[clienteId][0] += mensaje.cantidad
            self.clientes[clienteId][1] += 1

    def _procesarEOF(self, mensaje: FinMensajeSistema) -> None:
        print(f"Llego EOF {mensaje.clienteId}")
        
        promedio = self.clientes[str(mensaje.clienteId)][0] // self.clientes[str(mensaje.clienteId)][1] 
        
        nodo = mensaje.clienteId.int % TOTALCUENTAPROM

        self.exchangeCuentaProm[nodo].send(FinPromMensajeSistema(mensaje.clienteId, promedio).aBytes())

        del self.clientes[str(mensaje.clienteId)]
        

    def procesarMensaje(self, bytes, ack, nack):
        mensaje = recvMensajeSistema(bytes)
        if isinstance(mensaje, FinMensajeSistema): # TODO: esta bien esto?
            self._procesarEOF(mensaje)
        else:
            self._procesarData(mensaje)
        ack()

    def iniciar(self):
        self.exchangePromedio.start_consuming(self.procesarMensaje)

def main() -> int:
    promedio = Promedio()
    promedio.iniciar()
    return 0


if __name__ == "__main__":
    main()