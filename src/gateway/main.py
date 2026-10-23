import os
import uuid
import socket
import signal
import multiprocessing
from mensajesCliente import recvMensaje
from mensajesGateway import sendRespuesta, Respuesta1Mensaje
from mensajesSistema import FinMensajeSistema, Respuesta5MensajeSistema, LoteDataMensajeSistema, recvMensajeSistema
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
        try:
            respuesta = recvMensajeSistema(message)
            clienteId = respuesta.clienteId
            clienteSocket = clientes[clienteId]
            if isinstance(respuesta, FinMensajeSistema):
                print(f"LLego EOF {respuesta.clienteId}")
                # TODO: manejar EOF
                #sendRespuesta(clienteSocket, EOF)
                clientes[clienteId] = None
            else:
                sendRespuesta(clienteSocket, respuesta.aRespuestaGateway())
            ack()
        except Exception as e:
            print(e)
            nack()
        
    colaRespuestas.start_consuming(_consumirRespuesta)


def manejarSigterm(clientes: dict, serverSocket: socket.socket, sigtermRecivida) -> None:
    sigtermRecivida.value = 1
    serverSocket.shutdown(socket.SHUT_RDWR)
    for cliente in clientes.values():
        cliente.shutdown(socket.SHUT_RDWR)


def main() -> None:
    with multiprocessing.Manager() as manager:
        clientes = manager.dict()
        sigtermRecivida = manager.Value("c_short", 0)
        with multiprocessing.Pool(processes=os.process_cpu_count()) as processes_pool:
            processes_pool.apply_async(manejarRespuesta, args=(clientes,))

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serverSocket:
                serverSocket.bind(("0.0.0.0", GATEWAYPORT))
                serverSocket.listen()
                signal.signal(signal.SIGTERM, lambda signum, frame: manejarSigterm(clientes, serverSocket, sigtermRecivida))
                while True:
                    try:
                        clientSocket, _ = serverSocket.accept()
                        clientId = uuid.uuid4()
                        clientes[clientId] = clientSocket

                        processes_pool.apply_async(manejarPeticion, args=(clientId, clientSocket))
                    except socket.error:
                        if sigtermRecivida.value == 0:
                            return 1
                        else:
                            return 0
                    except Exception as e:
                        print(e)
                        return 2
    return 0


if __name__ == "__main__":
    main()