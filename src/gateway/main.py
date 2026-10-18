import os
import uuid
import socket
import multiprocessing
from mensajesCliente import recvMensaje
from mensajesGateway import sendRespuesta, recvMensajeSistema
from mensajesSistema import FinMensajeSistema, LoteDataMensajeSistema
from middleware import MessageMiddlewareQueue

MOMHOST = os.environ["MOMHOST"]
COLADATOS = os.environ["COLADATOS"]
COLARESPUESTAS = os.environ["COLARESPUESTAS"]

GATEWAYHOST = os.environ["GATEWAYHOST"]
GATEWAYPORT = int(os.environ["GATEWAYPORT"])
LOTE = int(os.environ["LOTE"])

def manejarPeticion(clienteId: uuid, clientSocket: socket.socket) -> None:
    try:
        colaDatos = MessageMiddlewareQueue(MOMHOST, COLADATOS)

        eof = False
        while not eof:
            mensaje = recvMensaje(clientSocket)
            if mensaje is None:
                eof = True
                colaDatos.send(FinMensajeSistema(clienteId).aBytes())
            else:
                colaDatos.send(LoteDataMensajeSistema(clienteId, mensaje).aBytes())
    except socket.error:
        print("The connection with the server was lost")
    except Exception as e:
        print(e)
    finally:
        colaDatos.close()


def manejarRespuesta(clientes: dict) -> None:
    colaRespuestas = MessageMiddlewareQueue(MOMHOST, COLARESPUESTAS)

    def _consumirRespuesta(message: bytes, ack, nack):
        clienteId, respuesta = recvMensajeSistema(message)
        clienteSocket = clientes[clienteId]
        if isinstance(respuesta, FinMensajeSistema):
            # TODO: manejar EOF
            #sendRespuesta(clienteSocket, EOF)
            clientes[clienteId] = None
        else:
            print(f"RESPUESTA: {respuesta.fecha}")
            sendRespuesta(clienteSocket, respuesta)
        ack()
        
    colaRespuestas.start_consuming(_consumirRespuesta)
    colaRespuestas.close()

def main() -> None:
    with multiprocessing.Manager() as manager:
        clientes = manager.dict()
        sigterm_received = manager.Value("c_short", 0)
        with multiprocessing.Pool(processes=os.process_cpu_count()) as processes_pool:
            processes_pool.apply_async(manejarRespuesta, args=clientes)

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
                server_socket.bind((GATEWAYHOST, GATEWAYPORT))
                server_socket.listen()
                while True:
                    try:
                        clientSocket, _ = server_socket.accept()
                        clientId = uuid.uuid4()
                        clientes[clientId] = clientSocket

                        processes_pool.apply_async(manejarPeticion, args=(clientId, clientSocket))
                    except socket.error:
                        if sigterm_received.value == 0:
                            return 1
                        else:
                            return 0
                    except Exception as e:
                        print(e)
                        return 2
    return 0


if __name__ == "__main__":
    main()