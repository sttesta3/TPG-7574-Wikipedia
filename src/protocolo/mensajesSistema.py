import uuid
from abc import ABC, abstractmethod
from mensajesCliente import DataMensaje 

FIN_MENSAJE =  b'\x00'
LOTE_MENSAJE = b'\x01'

class MensajeSistema(ABC):
    @abstractmethod
    def aBytes(self) -> bytes:
        pass

    @abstractmethod
    def deBytes(self, bytes: bytes) -> None:
        pass

class FinMensajeSistema(MensajeSistema):
    def __init__(self, clienteId: uuid = None) -> None:
        self.clienteId = clienteId
    

    def aBytes(self) -> bytes:
        mensajeBytes = FIN_MENSAJE
        mensajeBytes += self.clienteId.bytes
        return mensajeBytes
    

    def deBytes(self, bytes) -> None:
        self.clienteId = uuid.UUID(bytes)


class LoteDataMensajeSistema(MensajeSistema):
    def __init__(self, clienteId: uuid, lote: list[DataMensaje]) -> None:
        self.clienteId = clienteId
        self.lote = lote


    def aBytes(self) -> bytes:
        bytesMensaje = LOTE_MENSAJE
        bytesMensaje += len(self.lote).to_bytes(2, byteorder="big")
        bytesMensaje += self.clienteId.bytes
        
        dataMensajeBytes = b''
        for mensaje in self.lote:
            dataMensajeBytes += mensaje.aBytes()
        
        bytesMensaje += len(dataMensajeBytes).to_bytes(4, byteorder="big")
        bytesMensaje += dataMensajeBytes


    def deBytes(self, bytes: bytes) -> None:
        totalLeido = 0
        loteLen = int.from_bytes(bytes[totalLeido:totalLeido+2], byteorder="big")
        self.clienteId = uuid.UUID(bytes[totalLeido+2:totalLeido+18])
        totalLeido += 18

        for _ in range(loteLen):
            tamañoMensaje = int.from_bytes(bytes[totalLeido+1:totalLeido+5], byteorder="big")
            msg = DataMensaje()
            msg.deBytes(bytes[totalLeido+5:totalLeido+tamañoMensaje+5])
            self.lote.append(msg)
            totalLeido += tamañoMensaje + 5

        return self


def recvMensajeSistema(mensaje: bytes) -> MensajeSistema:
    ype = mensaje[1]

    rta = None

    if type == FIN_MENSAJE:
        rta = FinMensajeSistema()
    elif type == LOTE_MENSAJE:
        rta = LoteDataMensajeSistema()
    else:
        rta = None
    
    if rta is None:
        return None
    else:
        rta.deBytes(mensaje[1:])
        return rta