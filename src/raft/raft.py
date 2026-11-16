import os
import socket
import random
import logging
import threading
import multiprocessing
from socket.safeSocket import safeSend 
from protocolo.mensajesRaft import recvMensaje, VotacionMensaje, VotoMensaje, LatidoMensaje, RespuestaLatidoMensaje, LiderMensaje

ID = int(os.environ["ID"])
CANTIDADNODOS = int(os.environ["CANTIDADNODOS"])
RAFTHOST = os.environ["RAFTHOST"]
RAFTPORT = int(os.environ["RAFTPORT"])

SEGUIDOR = b'\x00'
CANDIDATO = b'\x01'
LIDER = b'\x03'

class raft():
    def __init__(self):
        self.id = ID
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
           safeSend(nodo, VotacionMensaje(self.id).aBytes())


    def contarVotos(self):
        if self.votos >= (CANTIDADNODOS / 2) + 1:
            self.estado = LIDER
            for nodo in self.nodos:
                safeSend(nodo, LiderMensaje(self.id).aBytes())
            self.latido()
        else:
            self.estado = SEGUIDOR
            self.timer = threading.Timer(random.randint(150, 300) / 1000, self.iniciarVotacion)
            self.timer.start()


    def latido(self):
        for nodo in self.nodos: 
            safeSend(nodo, LatidoMensaje(self.mensajes).aBytes())
        self.timer = threading.Timer(random.randint(150, 300) / 1000, self.latido)
        self.timer.start()
        self.mensajes = []


    def votacion(self, candidatoId: int) -> VotoMensaje:
        if self.voto is None:
            self.voto = candidatoId
            return VotoMensaje(1)
        return VotoMensaje(0)


    def nuevoLider(self, liderId: int):
        self.liderId = liderId
        self.voto = None
        self.votos = 0
        self.timer = threading.Timer(random.randint(150, 300) / 1000, self.iniciarVotacion)
        self.timer.start()


    def procesarMensaje(self, clientSocket: socket.socket):
        while True:
            mensaje = recvMensaje(clientSocket)

            if self.estado == SEGUIDOR:
                if isinstance(mensaje, VotacionMensaje):
                    safeSend(clientSocket, self.votacion(mensaje.candidatoId).aBytes())
                elif isinstance(mensaje, LatidoMensaje):
                    self.timer = threading.Timer(random.randint(150, 300) / 1000, self.iniciarVotacion)
                    # TODO: procesar mensaje
                    self.timer.start()
                elif isinstance(mensaje, LiderMensaje):
                    self.nuevoLider(mensaje.liderId)
            elif self.estado == CANDIDATO:
                if isinstance(mensaje, VotoMensaje):
                    self.votos += mensaje.voto
            elif self.estado == LIDER:
                if isinstance(mensaje, RespuestaLatidoMensaje):
                    # TODO: procesar mensaje
                    pass
            

    def iniciar(self):
        with multiprocessing.Pool(processes=os.process_cpu_count()) as processes_pool:
            self.socket.bind((RAFTHOST, RAFTPORT))
            self.timer.start()
            self.socket.listen()

            while True:
                try:
                    clientSocket, _ = self.socket.accept()  
                    processes_pool.apply_async(self.procesarMensaje, args=(clientSocket))
                except socket.error:
                    return 0
                except Exception as e:
                    logging.warning(e)
                    return 2