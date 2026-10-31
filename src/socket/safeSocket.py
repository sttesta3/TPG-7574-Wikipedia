import socket

def safeRecv(socket: socket.socket, size):
    bytes = b""
    recived = 0
    while recived < size:
        byte_rec = socket.recv(size - recived)
        if not byte_rec:
            raise ConnectionError("La conexion se cerro")

        recived += len(byte_rec)
        bytes += byte_rec

    return bytes

def safeSend(socket: socket.socket, bytes):
    bytes_send = 0 
    while bytes_send < len(bytes):
        try:
            sended = socket.send(bytes[bytes_send:])
            bytes_send += sended
        except Exception as e:
            return 0

    return bytes_send