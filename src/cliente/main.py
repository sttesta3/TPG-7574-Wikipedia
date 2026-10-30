import os
import sys
import socket
import signal
import threading
import pandas as pd
from protocolo.mensajesCliente import LoteMensaje, FinMensaje
from protocolo.mensajesGateway import recvMensaje, Respuesta1Mensaje, Respuesta2Mensaje, Respuesta5Mensaje

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
    while not eof:
        respuesta = recvMensaje(socket)

        # TODO: tal vez hacerlo mas polimorfico (?
        if isinstance(respuesta, FinMensaje):
            eof = True
        if isinstance(respuesta, Respuesta1Mensaje):
            with open("/output/output1.txt", "a", encoding="utf-8") as f:
                f.write(respuesta.url + " - "+ str(respuesta.fecha) + "\n")
        if isinstance(respuesta, Respuesta2Mensaje):
            with open("/output/output2.txt", "a", encoding="utf-8") as f:
                f.write(respuesta.nombre + " - "+respuesta.url + " - "+ str(respuesta.imgBytes) + "\n")
        if isinstance(respuesta, Respuesta4Mensaje):
            with open("/output/output4.txt", "a", encoding="utf-8") as f:
                for k,v in respuesta.palabras.items():
                    f.write(k +" - " +str(v) + "\n")
        if isinstance(respuesta, Respuesta5Mensaje):
            with open("/output/output5.txt", "a", encoding="utf-8") as f:
                f.write(respuesta.url + " - "+ str(respuesta.cantidad)+ "\n")
  

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
