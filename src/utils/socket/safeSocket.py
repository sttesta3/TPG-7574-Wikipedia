import socket
import logging

def safeRecv(socket: socket.socket, size):
    bytes = b""
    recived = 0
    logging.debug(f"[safe socket][recv] {recived} {bytes}")
    while recived < size:
        byte_rec = socket.recv(size - recived)
        logging.debug(f"[safe socket][recv] {recived} {bytes}")

        if not byte_rec:
            return bytes

        recived += len(byte_rec)
        bytes += byte_rec
    
    logging.debug("[safe socket][recv] FIN")
    return bytes

def safeSend(socket: socket.socket, bytes: bytes):
    bytes_send = 0 
    len_bytes = len(bytes)
    while bytes_send < len(bytes):
        logging.debug(f"[safe socket][send] {bytes_send} {len_bytes}")
        sended = socket.send(bytes[bytes_send:])
        bytes_send += sended

    return bytes_send
