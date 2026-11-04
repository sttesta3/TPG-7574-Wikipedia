import os
import sys
import logging
import socket
import signal
import threading
import pandas as pd
import pyarrow.parquet as pq
from protocolo.mensajesCliente import LoteMensaje, FinMensaje
from protocolo.mensajesGateway import recvMensaje, Respuesta1Mensaje, Respuesta2Mensaje, Respuesta3Mensaje, Respuesta4Mensaje, Respuesta5Mensaje

DATASETPATHEN = os.environ["DATASETPATHEN"]
DATASETPATHFR = os.environ["DATASETPATHFR"]
TOTALDATASETS = int(os.environ["TOTALDATASETS"])
GATEWAYHOST = os.environ["GATEWAYHOST"]
GATEWAYPORT = int(os.environ["GATEWAYPORT"])
LOTE = int(os.environ["LOTE"])
ID = os.environ["ID"]

def enviarParquet(socket: socket) -> None:
    loteMensaje = LoteMensaje(socket, LOTE)
    for i in range(TOTALDATASETS):

        archivo = pq.ParquetFile(DATASETPATHEN + str(i).zfill(5) + ".parquet")

        for batch in archivo.iter_batches(batch_size=10000):
            dataset = batch.to_pandas()

            for fila in dataset.itertuples(index=False):
                loteMensaje.agregarMensaje(fila)
            del dataset
        
        archivo = pq.ParquetFile(DATASETPATHFR + str(i).zfill(5) + ".parquet")

        for batch in archivo.iter_batches(batch_size=10000):
            dataset = batch.to_pandas()

            for fila in dataset.itertuples(index=False):
                loteMensaje.agregarMensaje(fila)
            del dataset

    loteMensaje.send()
    FinMensaje(socket).send()


def recibirRespuestas(socket: socket) -> None:
    eof = False
    while not eof:
        try:
            respuesta = recvMensaje(socket)
        except OSError as e:
            logging.error(f"Se perdio la conexion con el gateway: {e}")
            return
        
        archivos = [open(f"/output/output1_{ID}.txt", "a", encoding="utf-8"),
            open(f"/output/output2_{ID}.txt", "a", encoding="utf-8"),
            open(f"/output/output3_{ID}.txt", "a", encoding="utf-8"),
            open(f"/output/output4_{ID}.txt", "a", encoding="utf-8"),
            open(f"/output/output5_{ID}.txt", "a", encoding="utf-8")]

        if isinstance(respuesta, FinMensaje):
            eof = True
        if isinstance(respuesta, Respuesta1Mensaje):
            archivos[0].write(respuesta.url + " - "+ str(respuesta.fecha) + "\n")
        if isinstance(respuesta, Respuesta2Mensaje):
            archivos[1].write(respuesta.nombre + " - "+respuesta.url + " - "+ str(respuesta.imgBytes) + "\n")
        if isinstance(respuesta,Respuesta3Mensaje):
            for palabra in respuesta.palabras:
                archivos[2].write(palabra + "\n")        
        if isinstance(respuesta, Respuesta4Mensaje):
            for k,v in respuesta.palabras.items():
                archivos[3].write(k +" - " +str(v) + "\n")
        if isinstance(respuesta, Respuesta5Mensaje):
            for k,v in respuesta.data.items():
                archivos[4].write(k + " - "+ str(v)+ "\n")
  

def manejarSigterm(coneccion: socket.socket, ) -> None:
    coneccion.shutdown(socket.SHUT_RDWR)
    sys.exit(0)

# TODO: quedan los hilos huerfanos si hay sigterm
def main():
    logging.basicConfig(level=logging.INFO)
    coneccion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    coneccion.connect((GATEWAYHOST, GATEWAYPORT))
    signal.signal(signal.SIGTERM, lambda signum, frame: manejarSigterm(coneccion))

    logging.info("Iniciando cliente...")
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
