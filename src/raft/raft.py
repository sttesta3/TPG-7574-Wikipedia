import os
import socket
import random
import asyncio
from socket.safeSocket import safeSend 
from protocolo.mensajesRaft import recvMensaje, VotacionMensaje, VotoMensaje, LatidoMensaje, RespuestaLatidoMensaje, LiderMensaje, RaftMensaje

ID = int(os.environ["ID"])
CANTIDADNODOS = int(os.environ["CANTIDADNODOS"])
RAFTHOST = os.environ["RAFTHOST"]
RAFTPORT = int(os.environ["RAFTPORT"])

SEGUIDOR = b'\x00'
CANDIDATO = b'\x01'
LIDER = b'\x03'

class Timer():
    def __init__(self) -> None:
        self.loop = asyncio.get_running_loop()
        self.timer = None

    
    def setear(self, fn):
        if self.timer is not None:
            self.timer.cancel()

        self.timer = self.loop.call_later(random.randint(150, 300) / 1000, self.iniciarVotacion)
    

    def cancelar(self):
        self.timer.cancel()
        self.timer = None


class Raft():
    def __init__(self):
        self.id = ID
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        self.nodos = []

        self.estado = SEGUIDOR
        self.timer = Timer()

        self.votos = 0
        self.voto = None
        self.liderId = None

        self.mensajes = []


    def iniciarVotacion(self):
        self.timer.setear(self.contarVotos)
        self.estado = CANDIDATO
        self.votos = 1

        for nodo in self.nodos:
           safeSend(nodo, VotacionMensaje(self.id).aBytes())


    def contarVotos(self):
        if self.votos >= (CANTIDADNODOS // 2) + 1:
            self.estado = LIDER
            for nodo in self.nodos:
                safeSend(nodo, LiderMensaje(self.id).aBytes())
            self.latido()
        else:
            self.estado = SEGUIDOR
            self.timer.setear(self.iniciarVotacion)


    def latido(self):
        for nodo in self.nodos: 
            safeSend(nodo, LatidoMensaje(self.mensajes).aBytes())
        self.timer.setear(self.latido)
        self.mensajes = []


    def votacion(self, candidatoId: int) -> VotoMensaje:
        self.timer.setear(self.iniciarVotacion)
        if self.voto is None:
            self.voto = candidatoId
            return VotoMensaje(1)
        return VotoMensaje(0)


    def nuevoLider(self, liderId: int):
        self.liderId = liderId
        self.voto = None
        self.votos = 0
        self.timer.setear(self.iniciarVotacion)


    def procesarMensaje(self, clientWriter: asyncio.StreamWriter, mensaje: RaftMensaje):
        if self.estado == SEGUIDOR:
            if isinstance(mensaje, VotacionMensaje):
                clientWriter.write(self.votacion(mensaje.candidatoId).aBytes())
            elif isinstance(mensaje, LatidoMensaje):
                self.timer.setear(self.iniciarVotacion)
                # TODO: procesar mensaje
                
            elif isinstance(mensaje, LiderMensaje):
                self.nuevoLider(mensaje.liderId)
        elif self.estado == CANDIDATO:
            if isinstance(mensaje, VotoMensaje):
                self.votos += mensaje.voto
        elif self.estado == LIDER:
            if isinstance(mensaje, RespuestaLatidoMensaje):
                # TODO: procesar mensaje
                pass

    
    async def procesarConexion(self, reader, writer):
        while True:
            mensaje = await recvMensaje(reader)

            self.procesarMensaje(writer, mensaje)
            

    async def iniciar(self):
        server = await asyncio.start_server(self.procesarConexion, RAFTHOST, RAFTPORT)

        async with server:
            await server.serve_forever()