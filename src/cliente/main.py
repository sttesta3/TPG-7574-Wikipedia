import os
import socket
import pandas as pd
from mensajes import LoteMensaje

FILE = os.environ["FILE"]
GATEWAYHOST = os.environ["GATEWAYHOST"]
GATEWAYPORT = int(os.environ["GATEWAYPORT"])
LOTE = int(os.environ["LOTE"])

def _enviarParquet(socket: socket.socket) -> None:
    dataset =  pd.read_parquet(FILE)
    loteMensaje = LoteMensaje(LOTE, socket)

    for fila in dataset.itertuples():
        loteMensaje.agregarMensaje(fila)
    
    loteMensaje.send()


def _recibirRta(socket: socket.socket) -> None:
    pass


def main():
    #c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #coneccion = c.connect((GATEWAYHOST, GATEWAYPORT))
    _enviarParquet("coneccion")
    _recibirRta("coneccion")

if __name__ == "__main__":
    main()