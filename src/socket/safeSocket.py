import socket

def safeRecv(socket: socket.socket, size):
    bytes = b""
    recived = 0
    while recived < size:
        try:
            byte_rec = socket.recv(size - recived)

            if byte_rec == 0:
                return b""

            recived += len(byte_rec)
            bytes += byte_rec
        except Exception as e:
            return b""

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