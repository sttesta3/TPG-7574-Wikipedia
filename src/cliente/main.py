import os
import sys
import logging
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
    logging.info("Thread emisor iniciado")
    loteMensaje = LoteMensaje(socket, LOTE)
    for i in range(TOTALDATASETS):
        logging.info(f"Agrego dataset {i}")
        datasetEn = pd.read_parquet(DATASETPATHEN + str(i).zfill(5) + ".parquet")
        datasetFr = pd.read_parquet(DATASETPATHFR + str(i).zfill(5) + ".parquet")
        
        logging.info("Post pd.read_parquet")
        dataset = pd.concat([datasetEn, datasetFr])
        
        logging.info("Post pd.concat")
        cuenta = 0
        for fila in dataset.itertuples():
            logging.info(f"Agregando mensaje {cuenta} al lote")
            loteMensaje.agregarMensaje(fila)
            logging.info("Mensaje agregado OK")
            cuenta += 1 
    
    logging.info("Por enviar Lote")    
    loteMensaje.send()
    logging.info("Lote enviado")
    FinMensaje(socket).send()
    logging.info("EOF enviado")


def recibirRespuestas(socket: socket) -> None:
    logging.info("Thread receptor iniciado")
    eof = False
    while not eof:
        respuesta = recvMensaje(socket)
        logging.info(f"Recibi respuesta {respuesta}")        

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
