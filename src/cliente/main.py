import os
import sys
import logging
import socket
import signal
import threading
import time
import pyarrow.parquet as pq
from protocolo.mensajesCliente import LoteMensaje, FinMensaje
from protocolo.mensajesGateway import recvMensaje, Respuesta1Mensaje, Respuesta2Mensaje, Respuesta3Mensaje, Respuesta4Mensaje, Respuesta5Mensaje

DATASETPATHEN = os.environ["DATASETPATHEN"]
DATASETPATHFR = os.environ["DATASETPATHFR"]
TOTALDATASETSFR = int(os.environ["TOTALDATASETSFR"])
TOTALDATASETSEN = int(os.environ["TOTALDATASETSEN"])
GATEWAYHOST = os.environ["GATEWAYHOST"]
GATEWAYPORT = int(os.environ["GATEWAYPORT"])
LOTE = int(os.environ["LOTE"])
ID = os.environ["ID"]


def enviarParquet(socket: socket) -> None:
    try:
        inicio = time.time()
        loteMensaje = LoteMensaje(socket, LOTE)
        
        j = 0
        for i in range(TOTALDATASETSEN):

            with pq.ParquetFile(DATASETPATHEN + str(i).zfill(5) + ".parquet") as archivo:
                for batch in archivo.iter_batches(batch_size=10000):
                    dataset = batch.to_pandas()
                    for fila in dataset.itertuples(index=False):
                        loteMensaje.agregarMensaje(fila)
                    del dataset
                    del batch
            

            if j < TOTALDATASETSFR:
                with pq.ParquetFile(DATASETPATHFR + str(i).zfill(5) + ".parquet") as archivo:
                    for batch in archivo.iter_batches(batch_size=10000):
                        dataset = batch.to_pandas()

                        for fila in dataset.itertuples(index=False):
                            loteMensaje.agregarMensaje(fila)
                        del dataset
                        del batch

                    j += 1

            print(f"vamos por EN {i} - FR {j} en {(time.time() - inicio)/60:.2f}")

        loteMensaje.send()
        FinMensaje(socket).send()

        fin = time.time()
        print(f"Tiempo de envio de mensajes: {(fin - inicio)/60:.2f} minutos")

    except Exception as e:
        print(e)


def recibirRespuestas(socket: socket) -> None:
    inicio = time.time()
    eof = False
    archivos = [
        open(f"/output/output1_{ID}.txt", "a", encoding="utf-8"),
        open(f"/output/output2_{ID}.txt", "a", encoding="utf-8"),
        open(f"/output/output3_{ID}.txt", "a", encoding="utf-8"),
        open(f"/output/output4_{ID}.txt", "a", encoding="utf-8"),
        open(f"/output/output5_{ID}.txt", "a", encoding="utf-8")
    ]
    
    while not eof:
        try:
            respuesta = recvMensaje(socket)
        except OSError as e:
            logging.error(f"Se perdio la conexion con el gateway: {e}")
            return
        

        if isinstance(respuesta, FinMensaje):
            eof = True
            for archivo in archivos:
                archivo.close()
            
            print(f"fin {time.time()}")
            fin = time.time()
            print(f"Tiempo de envio de mensajes: {(fin - inicio)/60:.2f} minutos")
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
