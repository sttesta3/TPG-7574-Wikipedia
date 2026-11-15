import os
import time
import socket
import random
import logging
import threading
import multiprocessing
from socket.safeSocket import safeRecv, safeSend 
from protocolo.mensajesRaft import recvMensaje, mensajeVotacion, mensajeVoto, mensajeLatido, mensajeLider

CANTIDADNODOS = int(os.environ["CANTIDADNODOS"])
RAFTHOST = os.environ["RAFTHOST"]
RAFTPORT = int(os.environ["RAFTPORT"])

SEGUIDOR = b'\x00'
CANDIDATO = b'\x01'
LIDER = b'\x03'

class raft():
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        self.nodos = []

        self.estado = SEGUIDOR
        self.timer = threading.Timer(random.randint(150, 300) / 1000, self.iniciarVotacion)

        self.votos = 0
        self.voto = None
        self.liderId = None

        self.mensajes = []


    def iniciarVotacion(self):
        self.timer.cancel()
        self.estado = CANDIDATO
        self.votos += 1

        for nodo in self.nodos:
           #TODO: pedir votos
           pass 

        #TODO: Contar votos
        if self.votos >= (CANTIDADNODOS / 2) + 1:
            self.estado = LIDER
            for nodo in self.nodos:
                #TODO: me declaro lider
                pass 
            self.latido()
        else:
            self.timer = threading.Timer(random.randint(150, 300) / 1000, self.iniciarVotacion)
            self.timer.start()


    def latido(self):
        while self.estado == LIDER:
            for nodo in self.nodos:
                # TODO: usar lock para esto 
                safeSend(nodo, mensajeLatido(self.mensajes).aBytes())
            self.mensajes = []
            time.sleep(1)


    def votacion(self, candidatoId: int) -> int:
        if self.voto is None:
            self.voto = candidatoId
            return 1
        return 0


    def nuevoLider(self, liderId: int):
        self.liderId = liderId
        self.voto = None
        self.timer = threading.Timer(random.randint(150, 300) / 1000, self.iniciarVotacion)
        self.timer.start()


    def procesarMensaje(self, clientSocket: socket.socket):
        
        if self.estado == SEGUIDOR:
            mensaje = recvMensaje(clientSocket)
            
            if isinstance(mensaje, mensajeVotacion):
                safeSend(clientSocket, mensajeVoto(self.votacion()).aBytes())
            elif isinstance(mensaje, mensajeLatido):
                # TODO: procesar mensaje
                self.timer = threading.Timer(random.randint(150, 300) / 1000, self.iniciarVotacion)
                self.timer.start()
            elif isinstance(mensaje, mensajeLider):
                self.nuevoLider(mensaje.liderId)


    def iniciar(self):
        with multiprocessing.Pool(processes=os.process_cpu_count()) as processes_pool:
            self.socket.bind((RAFTHOST, RAFTPORT))
            self.timer.start()
            self.socket.listen()

            while True:
                try:
                    clientSocket, clientAddress = self.socket.accept()  
                    processes_pool.apply_async(self.procesarMensaje, args=(clientSocket))
                except socket.error:
                    return 0
                except Exception as e:
                    logging.warning(e)
                    return 2