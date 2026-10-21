import os
import socket
import pandas as pd
from mensajesCliente import LoteMensaje, FinMensaje
from mensajesGateway import recvMensaje

DATASETPATHEN = os.environ["DATASETPATHEN"]
DATASETPATHFR = os.environ["DATASETPATHFR"]
TOTALDATASETS = int(os.environ["TOTALDATASETS"])
GATEWAYHOST = os.environ["GATEWAYHOST"]
GATEWAYPORT = int(os.environ["GATEWAYPORT"])
LOTE = int(os.environ["LOTE"])

# TODO: tener un hilo enviando y otro recibiendo
def enviarParquet(socket: socket) -> None:
    loteMensaje = LoteMensaje(socket, LOTE)
    for i in range(TOTALDATASETS):
        datasetEn = pd.read_parquet(DATASETPATHEN + str(i).zfill(5) + ".parquet")
        datasetFr = pd.read_parquet(DATASETPATHFR + str(i).zfill(5) + ".parquet")

        dataset = pd.concat([datasetEn, datasetFr])

        for fila in dataset.itertuples():
            loteMensaje.agregarMensaje(fila)
        
    loteMensaje.send()
    FinMensaje(socket).send()
    print("Envio EOF")


def recibirRta(socket: socket) -> None:
    while True:
        a = recvMensaje(socket)

        #print(a.url)


def main():
    coneccion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    coneccion.connect((GATEWAYHOST, GATEWAYPORT))
    enviarParquet(coneccion)
    recibirRta(coneccion)

if __name__ == "__main__":
    main()