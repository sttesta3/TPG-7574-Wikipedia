import os
import uuid
import socket
import multiprocessing
from mensajesCliente import recvMensaje, DataMensaje

GATEWAYHOST = os.environ["GATEWAYHOST"]
GATEWAYPORT = int(os.environ["GATEWAYPORT"])
LOTE = int(os.environ["LOTE"])

def handle_client_request(clientId: uuid, clientSocket: socket.socket) -> None:
    try:
        print("llego algo")
        a = recvMensaje(clientSocket)
        
        print(a.nombre)

    except socket.error:
        print("The connection with the server was lost")
    except Exception as e:
        print(e)


def main() -> None:
    with multiprocessing.Manager() as manager:
        clients = manager.dict()
        sigterm_received = manager.Value("c_short", 0)
        with multiprocessing.Pool(processes=os.process_cpu_count()) as processes_pool:
            #processes_pool.apply_async(handle_client_response, (client_list,))

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
                server_socket.bind((GATEWAYHOST, GATEWAYPORT))
                server_socket.listen()
                while True:
                    try:
                        clientSocket, _ = server_socket.accept()
                        clientId = uuid.uuid4()
                        clients[clientId] = clientSocket

                        processes_pool.apply_async(handle_client_request, args=(clientId, clientSocket))
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