import uuid


class contadorEof():
    '''
    Lleva, por cliente, los lotes ya procesados (para descartar duplicados) y los EOFs recibidos
    de cada nodo de la etapa anterior.

    Cada nodo consume su propia cola, y cada nodo anterior manda sus datos y despues su EOF por el
    mismo canal, que RabbitMQ entrega en orden. Por eso, cuando llego el EOF de todos los nodos
    anteriores, ya llegaron (y se procesaron) todos los datos del cliente.
    '''

    def __init__(self, esperados: int) -> None:
        self.esperados = esperados
        self.procesados: dict[uuid.UUID, set[int]] = {}
        self.eofs: dict[uuid.UUID, set[int]] = {}
        self.finalizados: set[uuid.UUID] = set()


    def yaFinalizado(self, clienteId: uuid.UUID) -> bool:
        return clienteId in self.finalizados


    def yaProcesado(self, clienteId: uuid.UUID, secuencia: int) -> bool:
        return secuencia in self.procesados.get(clienteId, ())


    def procesado(self, clienteId: uuid.UUID, secuencia: int) -> None:
        self.procesados.setdefault(clienteId, set()).add(secuencia)


    def eofRecibido(self, clienteId: uuid.UUID, origen: int) -> bool:
        '''Registra el EOF de `origen`. Devuelve True una unica vez: cuando llego el de todos los nodos anteriores.'''
        if clienteId in self.finalizados:
            return False
        eofs = self.eofs.setdefault(clienteId, set())
        if origen in eofs:
            return False
        eofs.add(origen)
        return len(eofs) == self.esperados


    def finalizar(self, clienteId: uuid.UUID) -> None:
        self.finalizados.add(clienteId)
        self.procesados.pop(clienteId, None)
        self.eofs.pop(clienteId, None)


    def state(self) -> list:
        return [self.esperados, self.procesados, self.eofs, self.finalizados]


    def load_state(self, state: list):
        if len(state) == 4:
            self.esperados = state[0]
            self.procesados = {
                uuid.UUID(cliente): set(secuencias)
                for cliente, secuencias in state[1].items()
            }

            self.eofs = {
                uuid.UUID(cliente): set(origenes)
                for cliente, origenes in state[2].items()
            }

            self.finalizados = {
                uuid.UUID(cliente)
                for cliente in state[3]
            }