import socket
import logging

def safeRecv(socket: socket.socket, size):
    bytes = b""
    recived = 0
    logging.debug(f"[safe socket][recv] {recived} {bytes}")
    while recived < size:
        try:
            byte_rec = socket.recv(size - recived)
            logging.debug(f"[safe socket][recv] {recived} {bytes}")

            if not byte_rec:
                logging.warn(f"[safe socket][recv] leí cero, devuelvo lo leído")
                return bytes

            recived += len(byte_rec)
            bytes += byte_rec
        except Exception as e:
            logging.warn("[safe socket][recv] Excepcion {e}")
            return b""
    
    logging.debug("[safe socket][recv] FIN")
    return bytes

def safeSend(socket: socket.socket, bytes):
    bytes_send = 0 
    len_bytes = len(bytes)
    while bytes_send < len(bytes):
        logging.debug(f"[safe socket][send] {bytes_send} {len_bytes}")
        try:
            sended = socket.send(bytes[bytes_send:])
            logging.debug("[safe socket][send] send")
            bytes_send += sended
        except Exception as e:
            logging.warn("[safe socket][send] Excepcion {e}")
            return 0

    return bytes_send
