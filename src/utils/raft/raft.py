import os
import socket
import random
import asyncio 
from protocolo.mensajesRaft import recvMensaje, VotacionMensaje, VotoMensaje, LatidoMensaje, RespuestaLatidoMensaje, LiderMensaje, RaftMensaje

ID = int(os.environ["ID"])
CANTIDADNODOS = int(os.environ["CANTIDADNODOS"])
RAFTHOSTS = os.environ["RAFTHOSTS"]
RAFTPORT = int(os.environ["RAFTPORT"])

SEGUIDOR = b'\x00'
CANDIDATO = b'\x01'
LIDER = b'\x03'

LECTURA = 0
ESCRITURA = 1

class Timer():
    def __init__(self) -> None:
        self.loop = asyncio.get_running_loop()
        self.timer = None

    
    def _setear(self, min, max, fn):
        if self.timer is not None:
            self.timer.cancel()

        self.timer = self.loop.call_later(random.randint(min, max) / 1000,  lambda: asyncio.create_task(fn()))
    

    def setearLargo(self, fn):
        self._setear(500, 1000, fn)


    def setearMedio(self, fn):
        self._setear(150, 250, fn)
        

    def setearCorto(self, fn):
        self._setear(50, 100, fn)


    def cancelar(self):
        if self.timer is not None:
            self.timer.cancel()
        self.timer = None


class Raft():
    def __init__(self):
        self.id = ID
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        self.nodos = []
        
        self.estado = SEGUIDOR
        self.timer = None

        self.votos = 0
        self.voto = None
        self.liderId = None
        self.term = 0

        self.index = 0
        self.mensajes = []


    async def iniciarVotacion(self):
        self.term += 1
        self.estado = CANDIDATO
        self.votos = 1
        self.voto = self.id
        print(f"soy {self.id} e inicie la votacion")
        for nodo in self.nodos:
            try:
                nodo[ESCRITURA].write(VotacionMensaje(self.id, self.term, self.index).aBytes())
                await nodo[ESCRITURA].drain()
            except (ConnectionResetError, BrokenPipeError, OSError, asyncio.IncompleteReadError):
                pos = self.nodos.index(nodo)
                self.nodos.pop(pos)
                break
        self.timer.setearMedio(self.contarVotos)


    async def contarVotos(self):
        if self.votos >= (CANTIDADNODOS // 2) + 1:
            print(f"soy {self.id} y gane")
            self.estado = LIDER
            for nodo in self.nodos:
                try:
                    nodo[ESCRITURA].write(LiderMensaje(self.id, self.term).aBytes()) 
                    await nodo[ESCRITURA].drain()
                except (ConnectionResetError, BrokenPipeError, OSError, asyncio.IncompleteReadError):
                    pos = self.nodos.index(nodo)
                    self.nodos.pop(pos)
                    break
            self.timer.setearCorto(self.latido)
        else:
            self.timer.setearLargo(self.iniciarVotacion)
            print(f"soy {self.id} y perdi, me votaron {self.votos}")
            self.estado = SEGUIDOR


    async def latido(self):
        for nodo in self.nodos: 
            try:
                nodo[ESCRITURA].write(LatidoMensaje(self.mensajes).aBytes()) 
                await nodo[ESCRITURA].drain()
            except (ConnectionResetError, BrokenPipeError, OSError, asyncio.IncompleteReadError):
                pos = self.nodos.index(nodo)
                self.nodos.pop(pos)
                break
        self.timer.setearCorto(self.latido)
        self.mensajes = []


    def votacion(self, mensaje: VotacionMensaje) -> VotoMensaje:
        self.timer.setearLargo(self.iniciarVotacion)
        
        if (self.voto is None or self.term < mensaje.term) and self.index <= mensaje.index:
            print(f"soy {self.id} y voto por {mensaje.candidatoId}")
            self.term = mensaje.term
            self.voto = mensaje.candidatoId
            self.estado = SEGUIDOR
            return VotoMensaje(1, self.term)

        return VotoMensaje(0, self.term)


    def nuevoLider(self, mensaje: LiderMensaje):
        self.timer.setearLargo(self.iniciarVotacion)
        print(f"soy {self.id} y gano como lider {mensaje.liderId}")
        self.liderId = mensaje.liderId
        self.term = mensaje.term
        self.voto = None
        self.votos = 0
        self.estado = SEGUIDOR


    async def procesarMensaje(self, clientWriter: asyncio.StreamWriter, mensaje: RaftMensaje):
        
        if isinstance(mensaje, VotacionMensaje):
            clientWriter.write(self.votacion(mensaje).aBytes())
            await clientWriter.drain()          
        elif isinstance(mensaje, LatidoMensaje):
            self.timer.setearLargo(self.iniciarVotacion)
            # TODO: procesar mensaje
        elif isinstance(mensaje, LiderMensaje):
            self.nuevoLider(mensaje)
        elif isinstance(mensaje, VotoMensaje):
            if mensaje.term == self.term and self.estado == CANDIDATO:
                self.votos += mensaje.voto
        elif isinstance(mensaje, RespuestaLatidoMensaje):
                
                # TODO: procesar mensaje

                pass

    
    async def procesarConexion(self, reader, writer):
        if (reader, writer) not in self.nodos:
            self.nodos.append((reader, writer))

        while True:
            try:
                mensaje = await recvMensaje(reader)
                await self.procesarMensaje(writer, mensaje)
            except (ConnectionResetError, BrokenPipeError, OSError, asyncio.IncompleteReadError):
                nodo = self.nodos.index((reader, writer))
                self.nodos.pop(nodo)
                break
            except Exception:
                continue
                
            
    async def conectarNodos(self):
        hosts = os.getenv("RAFTHOSTS", "").split(",")
        for host in hosts:
            if host is not None and host != "":
                try:
                    reader, writer = await asyncio.open_connection(host, RAFTPORT)
                    print(f"me conecto con {host}")
                    asyncio.create_task(self.procesarConexion(reader, writer))
                except Exception:
                    continue


    async def iniciar(self):
        self.timer = Timer()
        self.timer.setearCorto(self.iniciarVotacion)

        server = await asyncio.start_server(self.procesarConexion, host="0.0.0.0",  port=RAFTPORT)

        async with server:
            await self.conectarNodos()
            await server.serve_forever()

    def iniciarRaft(self):
        asyncio.run(self.iniciar())