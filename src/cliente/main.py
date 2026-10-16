import os
import socket
import pandas as pd
from mensajes import LoteMensaje, FinMensaje

DATASETPATH = os.environ["DATASETPATH"]
TOTALDATASET = int(os.environ["TOTALDATASET"])
GATEWAYHOST = os.environ["GATEWAYHOST"]
GATEWAYPORT = int(os.environ["GATEWAYPORT"])
LOTE = int(os.environ["LOTE"])


def enviarParquet(socket: socket) -> None:
    for i in range(TOTALDATASET):
        dataset =  pd.read_parquet(DATASETPATH+ str(i).zfill(5) + ".parquet")
        loteMensaje = LoteMensaje(socket, LOTE)

        for fila in dataset.itertuples():
            loteMensaje.agregarMensaje(fila)
        
        loteMensaje.send()
        FinMensaje(socket).send()
        while True:
            continue


def recibirRta(socket: socket) -> None:
    pass


def main():
    coneccion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    coneccion.connect((GATEWAYHOST, GATEWAYPORT))
    enviarParquet(coneccion)
    recibirRta(coneccion)

if __name__ == "__main__":
    main()