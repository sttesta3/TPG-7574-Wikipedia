import os
import socket
import pandas as pd
from mensajes import LoteMensaje, FinMensaje

FILE = os.environ["FILE"]
GATEWAYHOST = os.environ["GATEWAYHOST"]
GATEWAYPORT = int(os.environ["GATEWAYPORT"])
LOTE = int(os.environ["LOTE"])

def _enviarParquet(socket: socket) -> None:
    dataset =  pd.read_parquet(FILE)
    loteMensaje = LoteMensaje(socket, LOTE)

    for fila in dataset.itertuples():
        loteMensaje.agregarMensaje(fila)
        break
    
    loteMensaje.send()
    FinMensaje(socket).send()

    while True:
        continue


def _recibirRta(socket: socket) -> None:
    pass


def main():
    coneccion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    coneccion.connect((GATEWAYHOST, GATEWAYPORT))
    _enviarParquet(coneccion)
    _recibirRta(coneccion)

if __name__ == "__main__":
    main()