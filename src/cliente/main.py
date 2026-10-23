import os
import sys
import socket
import signal
import threading
import pandas as pd
from mensajesCliente import LoteMensaje, FinMensaje
from mensajesGateway import recvMensaje, Respuesta1Mensaje, Respuesta2Mensaje, Respuesta5Mensaje

DATASETPATHEN = os.environ["DATASETPATHEN"]
DATASETPATHFR = os.environ["DATASETPATHFR"]
TOTALDATASETS = int(os.environ["TOTALDATASETS"])
GATEWAYHOST = os.environ["GATEWAYHOST"]
GATEWAYPORT = int(os.environ["GATEWAYPORT"])
LOTE = int(os.environ["LOTE"])

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


def recibirRespuestas(socket: socket) -> None:
    eof = False
    i = 0
    while not eof:
        respuesta = recvMensaje(socket)

        if isinstance(respuesta, Respuesta2Mensaje):
            i += 1
            print(i)


def manejarSigterm(coneccion: socket.socket, ) -> None:
    coneccion.shutdown(socket.SHUT_RDWR)
    sys.exit(0)

# TODO: quedan los hilos huerfanos si hay sigterm
def main():
    coneccion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    coneccion.connect((GATEWAYHOST, GATEWAYPORT))
    signal.signal(signal.SIGTERM, lambda signum, frame: manejarSigterm(coneccion))

    emisor = threading.Thread(
        target=enviarParquet,
        args=(coneccion,),
        daemon=True
    )

    receptor = threading.Thread(
        target=recibirRespuestas,
        args=(coneccion,),
        daemon=True
    )

    emisor.start()
    receptor.start()

    emisor.join()
    receptor.join()


if __name__ == "__main__":
    main()