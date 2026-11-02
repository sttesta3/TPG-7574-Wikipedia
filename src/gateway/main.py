import os
import uuid
import logging
import socket
import signal
import multiprocessing
from protocolo.mensajesCliente import recvMensaje, FinMensaje
from protocolo.mensajesGateway import sendRespuesta
from protocolo.mensajesSistema import FinMensajeSistema, LoteDataMensajeSistema, recvMensajeSistema
from middleware import MessageMiddlewareQueue

GATEWAYHOST = os.environ["GATEWAYHOST"]
GATEWAYPORT = int(os.environ["GATEWAYPORT"])
LOTE = int(os.environ["LOTE"])
MOMHOST = os.environ["MOMHOST"]
COLADATOS = os.environ["COLADATOS"]
COLARESPUESTAS = os.environ["COLARESPUESTAS"]

TOTALIMGEOF = int(os.environ["TOTALIMGEOF"])
TOTALPROMEOF = int(os.environ["TOTALPROMEOF"])
TOTALTOPEOF = int(os.environ["TOTALTOPEOF"])

def manejarPeticion(clienteId: uuid, clientSocket: socket.socket) -> None:
    logging.basicConfig(level=logging.INFO)
    logging.info(f"manejando cliente {clienteId}")
    try:
        colaDatos = MessageMiddlewareQueue(MOMHOST, COLADATOS)
        
        eof = False
        while not eof:
            logging.debug("Marcador loop recepcion")
            mensaje = recvMensaje(clientSocket)
            if mensaje is None:
                eof = True
                logging.debug(f"Cliente {clienteId} envio eof")
                colaDatos.send(FinMensajeSistema(clienteId).aBytes())
                logging.debug(f"EOF cliente {clienteId} enviado OK")
            else:
                logging.debug(f"Cliente {clienteId} mensaje {mensaje}")
                colaDatos.send(LoteDataMensajeSistema(clienteId, mensaje).aBytes())
                logging.debug("Enviado")
    except socket.error:
        logging.error("The connection with the server was lost")
    except Exception as e:
        logging.warning(e)
    finally:
        colaDatos.close()


def manejarRespuesta(clientes: dict) -> None:
    colaRespuestas = MessageMiddlewareQueue(MOMHOST, COLARESPUESTAS)
    def _consumirRespuesta(message: bytes, ack, nack):
        try:
            respuesta = recvMensajeSistema(message)
            clienteId = respuesta.clienteId
            clienteSocket = clientes[clienteId][0]
            if isinstance(respuesta, FinMensajeSistema):
                cliente = clientes[clienteId]
                cliente[1] += 1
                clientes[clienteId] = cliente
                logging.debug(f"LLego EOF {respuesta.clienteId} - {clientes[clienteId][1]}")
                if clientes[clienteId][1] == TOTALIMGEOF + TOTALPROMEOF + TOTALTOPEOF:
                    FinMensaje(clienteSocket).send()
                    del clientes[clienteId]
            else:
                sendRespuesta(clienteSocket, respuesta.aRespuestaGateway())
            ack()
        except Exception as e:
            logging.info(e)
            nack()
        
    colaRespuestas.start_consuming(_consumirRespuesta)


def manejarSigterm(clientes: dict, serverSocket: socket.socket, sigtermRecivida) -> None:
    sigtermRecivida.value = 1
    serverSocket.shutdown(socket.SHUT_RDWR)
    for cliente in clientes.values():
        cliente.shutdown(socket.SHUT_RDWR)


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    with multiprocessing.Manager() as manager:
        clientes = manager.dict()
        sigtermRecivida = manager.Value("c_short", 0)
        with multiprocessing.Pool(processes=os.process_cpu_count()) as processes_pool:
            processes_pool.apply_async(manejarRespuesta, args=(clientes,))

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serverSocket:
                serverSocket.bind(("0.0.0.0", GATEWAYPORT))
                serverSocket.listen()
                logging.info(f"Servidor escuchando en 0.0.0.0:{GATEWAYPORT}")
                signal.signal(signal.SIGTERM, lambda signum, frame: manejarSigterm(clientes, serverSocket, sigtermRecivida))
                while True:
                    try:
                        clientSocket, clientAddress = serverSocket.accept()
                        if clientAddress[0] == '127.0.0.1':
                            logging.debug("HEALTHCHECK recibido OK. Ignorado")
                        else: 
                            clientId = uuid.uuid4()
                            clientes[clientId] = [clientSocket, 0]
                            
                            logging.info(f"Cliente aceptado {clientId} {clientSocket}")
                            processes_pool.apply_async(manejarPeticion, args=(clientId, clientSocket))
                    except socket.error:
                        if sigtermRecivida.value == 0:
                            return 1
                        else:
                            return 0
                    except Exception as e:
                        logging.warning(e)
                        return 2
    return 0


if __name__ == "__main__":
    main()
