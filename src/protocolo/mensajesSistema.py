import uuid
from abc import ABC, abstractmethod
from mensajesCliente import DataMensaje, FIN_MENSAJE
from mensajesGateway import Respuesta1Mensaje, Respuesta2Mensaje, Respuesta5Mensaje

RESPUESTA1_MENSAJE = b'\x01'
RESPUESTA2_MENSAJE = b'\x02'
RESPUESTA3_MENSAJE = b'\x03'
RESPUESTA4_MENSAJE = b'\x04'
RESPUESTA5_MENSAJE = b'\x05'

LOTE_DATA_MENSAJE = b'\x06'
IMG_MENSAJE = b'\x07'
TRANFORMADOR_MENSAJE = b'\x08'
PALABRAS_MENSAJE = b'\x09'
CANTIDAD_PALABRAS_MENSAJE = b'\x0A'
FIN_PROM_MENSAJE = b'\x0B'


class MensajeSistema(ABC):
    @abstractmethod
    def aBytes(self) -> bytes:
        pass

    @abstractmethod
    def deBytes(self, bytes: bytes) -> None:
        pass


class FinMensajeSistema(MensajeSistema):
    def __init__(self, clienteId: uuid.UUID = None) -> None:
        self.clienteId = clienteId
    

    def aBytes(self) -> bytes:
        mensajeBytes = FIN_MENSAJE
        mensajeBytes += self.clienteId.bytes
        return mensajeBytes
    

    def deBytes(self, bytes):
        self.clienteId = uuid.UUID(bytes = bytes)


class LoteDataMensajeSistema(MensajeSistema):
    def __init__(self, clienteId: uuid.UUID = None, lote: list[DataMensaje] = None) -> None:
        self.clienteId = clienteId
        self.lote = lote


    def aBytes(self) -> bytes:
        bytesMensaje = LOTE_DATA_MENSAJE
        bytesMensaje += len(self.lote).to_bytes(2, byteorder="big")
        bytesMensaje += self.clienteId.bytes

        dataMensajeBytes = b''
        for mensaje in self.lote:
            dataMensajeBytes += mensaje.aBytes()
        
        bytesMensaje += dataMensajeBytes

        return bytesMensaje


    def deBytes(self, bytes: bytes) -> None:
        loteLen = int.from_bytes(bytes[0:2], byteorder="big")
        self.clienteId = uuid.UUID(bytes=(bytes[2:18]))
        totalLeido = 18

        self.lote = []
        for _ in range(loteLen):
            tamañoMensaje = int.from_bytes(bytes[totalLeido+1:totalLeido+5], byteorder="big")
            msg = DataMensaje()
            msg.deBytes(bytes[totalLeido+5:totalLeido+tamañoMensaje+5])
            self.lote.append(msg)
            totalLeido += tamañoMensaje + 5

# TODO: implementarlo en lotes (si es considerado necesario)
class ImgMensajeSistema(MensajeSistema):
    def __init__(self, clienteId: uuid.UUID = None, url: str = None, nombre: str = None, imgUrl: str = None) -> None:
        self.clienteId = clienteId
        self.url = url
        self.nombre = nombre 
        self.imgUrl = imgUrl


    def aBytes(self) -> bytes:
        bytesMensaje = IMG_MENSAJE
        bytesMensaje += self.clienteId.bytes

        urlBytes = self.url.encode("UTF-8")
        bytesMensaje += len(urlBytes).to_bytes(4, byteorder="big")
        bytesMensaje += urlBytes

        nombreBytes = self.nombre.encode("UTF-8")
        bytesMensaje += len(nombreBytes).to_bytes(4, byteorder="big")
        bytesMensaje += nombreBytes

        imgUrlBytes = self.imgUrl.encode("UTF-8")
        bytesMensaje += len(self.imgUrl).to_bytes(4, "big")
        bytesMensaje += imgUrlBytes

        return bytesMensaje


    def deBytes(self, bytes: bytes) -> None:
        self.clienteId = uuid.UUID(bytes=(bytes[0:16]))
        totalLeido = 16

        urlLen = int.from_bytes(bytes[totalLeido:totalLeido+4], byteorder="big")
        self.url = bytes[totalLeido+4:totalLeido+urlLen+4].decode()
        totalLeido += (urlLen+4)

        nombreLen = int.from_bytes(bytes[totalLeido:totalLeido+4], byteorder="big")
        self.nombre = bytes[totalLeido+4:totalLeido+nombreLen+4].decode()
        totalLeido += (nombreLen + 4)

        imgUrlLen = int.from_bytes(bytes[totalLeido:totalLeido+4], byteorder="big")
        self.imgUrl = bytes[totalLeido+4:imgUrlLen+totalLeido+4].decode()


# TODO: implementarlo en lotes (si es considerado necesario)
class TransformadorMensajeSistema(MensajeSistema):
    def __init__(self, clienteId: uuid.UUID = None, url: str = None, fecha: int = None, resumen: str = None, lenguaje: int = None ):
        self.clienteId = clienteId
        self.url = url
        self.fecha = fecha
        self.resumen = resumen
        self.lenguaje = lenguaje


    def aBytes(self) -> bytes:
        bytesMensaje = TRANFORMADOR_MENSAJE

        urlBytes = self.url.encode("UTF-8")
        bytesMensaje += len(urlBytes).to_bytes(4, byteorder="big")
        bytesMensaje += urlBytes

        bytesMensaje += self.fecha.to_bytes(2, byteorder="big")

        resumenBytes = self.resumen.encode("UTF-8")
        bytesMensaje += len(resumenBytes).to_bytes(4, byteorder="big")
        bytesMensaje += resumenBytes

        bytesMensaje += self.lenguaje.to_bytes(2, byteorder="big")

        bytesMensaje += self.clienteId.bytes
        
        return bytesMensaje


    def deBytes(self, bytes) -> None:
        totalLeido = 0

        urlLen = int.from_bytes(bytes[totalLeido:totalLeido+4], byteorder="big")
        self.url = bytes[totalLeido+4:totalLeido+urlLen+4].decode()
        totalLeido += (urlLen+4)

        self.fecha = int.from_bytes(bytes[totalLeido:totalLeido+2], byteorder="big")
        totalLeido += 2

        resumenLen = int.from_bytes(bytes[totalLeido:totalLeido+4], byteorder="big")
        self.resumen = bytes[totalLeido+4:totalLeido+resumenLen+4].decode()
        totalLeido += (resumenLen+4)

        self.lenguaje = int.from_bytes(bytes[totalLeido:totalLeido+2], byteorder="big")
        totalLeido += 2

        self.clienteId = uuid.UUID(bytes=(bytes[totalLeido:totalLeido+16]))


class PalabrasMensajeSistema(MensajeSistema):
    def __init__(self, clienteId: uuid.UUID = None, url: str = None, lenguaje: int = None, palabras: dict[str,int] = None) -> None:
        self.clienteId = clienteId
        self.url = url
        self.lenguaje = lenguaje
        self.palabras = palabras

    
    def aBytes(self) -> bytes:
        mensajeBytes = PALABRAS_MENSAJE

        urlBytes = self.url.encode("UTF-8")
        mensajeBytes += len(urlBytes).to_bytes(4, byteorder="big")
        mensajeBytes += urlBytes

        mensajeBytes += self.lenguaje.to_bytes(2, byteorder="big")

        palabraTotal = []
        for clave, valor in self.palabras.items():
            palabraTotal.append(clave)
            palabraTotal.append(str(valor)) 

        palabrasBytes = ",".join(palabraTotal).encode("UTF-8")
        mensajeBytes += len(palabrasBytes).to_bytes(4, byteorder="big")
        mensajeBytes += palabrasBytes

        mensajeBytes += self.clienteId.bytes

        return mensajeBytes
    

    def deBytes(self, bytes: bytes) -> None:
        totalLeido = 0

        urlLen = int.from_bytes(bytes[totalLeido:totalLeido+4], byteorder="big")
        self.url = bytes[totalLeido+4:totalLeido+urlLen+4].decode()
        totalLeido += (urlLen + 4)

        self.lenguaje = int.from_bytes(bytes[totalLeido:totalLeido+2], byteorder="big")
        totalLeido += 2

        palabrasLen = int.from_bytes(bytes[totalLeido:totalLeido+4], byteorder="big")
        palabras = bytes[totalLeido+4:totalLeido+palabrasLen+4].decode()
        self.palabras = {}
        palabras = palabras.split(",")
        for i in range(0, len(palabras), 2):
            clave = palabras[i]
            valor = int(palabras[i + 1])
            self.palabras[clave] = valor
        
        totalLeido += (palabrasLen + 4)

        self.clienteId = uuid.UUID(bytes=(bytes[totalLeido:totalLeido+16]))


class CantidadPalabraMensajeSistema(MensajeSistema):
    def __init__(self, clienteId: uuid.UUID = None, url: str = None, cantidad : int = None) -> None:
        self.clienteId = clienteId
        self.url = url
        self.cantidad = cantidad

    
    def aBytes(self) -> bytes:
        mensajeBytes = CANTIDAD_PALABRAS_MENSAJE

        urlBytes = self.url.encode("UTF-8")
        mensajeBytes += len(urlBytes).to_bytes(4, byteorder="big")
        mensajeBytes += urlBytes

        mensajeBytes += self.cantidad.to_bytes(4, byteorder="big")

        mensajeBytes += self.clienteId.bytes

        return mensajeBytes
    

    def deBytes(self, bytes: bytes) -> None:
        totalLeido = 0

        urlLen = int.from_bytes(bytes[totalLeido:totalLeido+4], byteorder="big")
        self.url = bytes[totalLeido+4:totalLeido+urlLen+4].decode()
        totalLeido += (urlLen + 4)

        self.cantidad = int.from_bytes( bytes[totalLeido:totalLeido+4], byteorder="big")
        totalLeido += 4

        self.clienteId = uuid.UUID(bytes=(bytes[totalLeido:totalLeido+16]))


class FinPromMensajeSistema(MensajeSistema):
    def __init__(self, clienteId: uuid.UUID = None, promedio: int = None ):
        self.clienteId= clienteId
        self.promedio = promedio

    
    def aBytes(self) -> bytes:
        bytesMensaje = FIN_PROM_MENSAJE

        bytesMensaje += self.promedio.to_bytes(4, byteorder="big")

        bytesMensaje += self.clienteId.bytes

        return bytesMensaje
    

    def deBytes(self, bytes: bytes) -> None:
        
        self.promedio = int.from_bytes(bytes[0:4], byteorder="big")
        totalLeido = 4

        self.clienteId = uuid.UUID(bytes=bytes[totalLeido:totalLeido+16])


# TODO: implementarlo en lotes (si es considerado necesario)
class Respuesta1MensajeSistema(MensajeSistema):
    def __init__(self, clienteId: uuid.UUID = None , url: str = None, fecha: int = None):
        self.url = url
        self.fecha = fecha
        self.clienteId = clienteId


    def aBytes(self) -> bytes:
        bytesMensaje = RESPUESTA1_MENSAJE
        bytesMensaje += (Respuesta1Mensaje(self.url, self.fecha).aBytes())[1:]
        bytesMensaje += self.clienteId.bytes

        return bytesMensaje


    def deBytes(self, bytes) -> None:
        rtaMsg = Respuesta1Mensaje()
        rtaMsg.deBytes(bytes[4:len(bytes)-16])
        self.fecha = rtaMsg.fecha
        self.url = rtaMsg.url
        self.clienteId = uuid.UUID(bytes=bytes[len(bytes)-16:])


    def aRespuestaGateway(self) -> Respuesta1Mensaje:
        return Respuesta1Mensaje(self.url, self.fecha)

#TODO: implementarlo en lotes (si es considerado necesario)
class Respuesta2MensajeSistema(MensajeSistema):
    def __init__(self, clienteId: uuid.UUID = None, url: str = None, nombre: str = None, imgBytes: bytes = None):
        self.clienteId = clienteId
        self.url = url
        self.nombre = nombre
        self.imgBytes = imgBytes


    def aBytes(self) -> bytes:
        bytesMensaje = RESPUESTA2_MENSAJE
        bytesMensaje += (Respuesta2Mensaje(self.nombre, self.url, self.imgBytes).aBytes())[1:]
        bytesMensaje += self.clienteId.bytes

        return bytesMensaje


    def deBytes(self, bytes: bytes) -> None:
        rtaMsg = Respuesta2Mensaje()
        rtaMsg.deBytes(bytes[4:len(bytes)-16])
        self.nombre = rtaMsg.nombre
        self.imgBytes = rtaMsg.imgBytes
        self.url = rtaMsg.url

        self.clienteId = uuid.UUID(bytes=bytes[len(bytes)-16:])


    def aRespuestaGateway(self) -> Respuesta2Mensaje:
        return Respuesta2Mensaje(self.nombre, self.url, self.imgBytes) 

class Respuesta2MensajeSistema(MensajeSistema):
    def __init__(self, clienteId: uuid.UUID = None, url: str = None, nombre: str = None, imgBytes: bytes = None):
        self.clienteId = clienteId
        self.url = url
        self.nombre = nombre
        self.imgBytes = imgBytes


    def aBytes(self) -> bytes:
        bytesMensaje = RESPUESTA2_MENSAJE
        bytesMensaje += (Respuesta2Mensaje(self.nombre, self.url, self.imgBytes).aBytes())[1:]
        bytesMensaje += self.clienteId.bytes

        return bytesMensaje


    def deBytes(self, bytes: bytes) -> None:
        rtaMsg = Respuesta2Mensaje()
        rtaMsg.deBytes(bytes[4:len(bytes)-16])
        self.nombre = rtaMsg.nombre
        self.imgBytes = rtaMsg.imgBytes
        self.url = rtaMsg.url

        self.clienteId = uuid.UUID(bytes=bytes[len(bytes)-16:])


    def aRespuestaGateway(self) -> Respuesta2Mensaje:
        return Respuesta2Mensaje(self.nombre, self.url, self.imgBytes) 

class Respuesta3MensajeSistema(MensajeSistema):
    def __init__(self, clienteId: uuid.UUID = None, url: str = None, palabras: [str] = None):
        pass
    
    def aBytes(self) -> bytes:
        pass
    

    def deBytes(self, bytes) -> None:
        pass


    def aRespuestaGateway(self) -> Respuesta5Mensaje:
        pass

# TODO: implementarlo en lotes (si es considerado necesario)
class Respuesta5MensajeSistema(MensajeSistema):
    def __init__(self, clienteId: uuid.UUID = None, url: str = None, cantidad: int = None):
        self.clienteId  = clienteId
        self.url = url
        self.cantidad = cantidad

    
    def aBytes(self) -> bytes:
        bytesMensaje = RESPUESTA5_MENSAJE
        bytesMensaje += (Respuesta5Mensaje(self.url, self.cantidad).aBytes())[1:]
        bytesMensaje += self.clienteId.bytes

        return bytesMensaje
    

    def deBytes(self, bytes) -> None:
        rtamsg = Respuesta5Mensaje()
        rtamsg.deBytes(bytes[4:len(bytes)-16])
        self.url = rtamsg.url
        self.cantidad = rtamsg.cantidad
        self.clienteId = uuid.UUID(bytes=bytes[len(bytes)-16:])


    def aRespuestaGateway(self) -> Respuesta5Mensaje:
        return Respuesta5Mensaje(self.url, self.cantidad)


def recvMensajeSistema(mensaje: bytes) -> MensajeSistema:
    type = mensaje[:1]
    rta = None
    
    if type == FIN_MENSAJE:
        rta = FinMensajeSistema()
    elif type == LOTE_DATA_MENSAJE:
        rta = LoteDataMensajeSistema()
    elif type == TRANFORMADOR_MENSAJE:
        rta = TransformadorMensajeSistema()
    elif type == PALABRAS_MENSAJE:
        rta = PalabrasMensajeSistema()
    elif type == CANTIDAD_PALABRAS_MENSAJE:
        rta = CantidadPalabraMensajeSistema()
    elif type == IMG_MENSAJE:
        rta = ImgMensajeSistema()
    elif type == FIN_PROM_MENSAJE:
        rta = FinPromMensajeSistema()
    elif type == RESPUESTA1_MENSAJE:
        rta = Respuesta1MensajeSistema() 
    elif type == RESPUESTA2_MENSAJE:
        rta = Respuesta2MensajeSistema()
    elif type == RESPUESTA5_MENSAJE:
        rta = Respuesta5MensajeSistema()
    else:
        rta = None
    
    if rta is None:
        return None
    else:
        rta.deBytes(mensaje[1:])
        return rta