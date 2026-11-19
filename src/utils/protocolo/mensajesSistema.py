import uuid
from abc import ABC, abstractmethod
from protocolo.mensajesCliente import DataMensaje, FIN_MENSAJE
from protocolo.mensajesGateway import Respuesta1Mensaje, Respuesta2Mensaje, Respuesta3Mensaje,Respuesta4Mensaje, Respuesta5Mensaje

RESPUESTA1_MENSAJE = b'\x01'
RESPUESTA2_MENSAJE = b'\x02'
RESPUESTA3_MENSAJE = b'\x03'
RESPUESTA4_MENSAJE = b'\x04'
RESPUESTA5_MENSAJE = b'\x05'

LOTE_DATA_MENSAJE = b'\x06'
IMG_MENSAJE = b'\x07'
LOTE_TRANFORMADOR_MENSAJE = b'\x08'
LOTE_PALABRAS_MENSAJE = b'\x09'
LOTE_CANTIDAD_PALABRAS_MENSAJE = b'\x0A'
FIN_PROM_MENSAJE = b'\x0B'
LOTE_IMG_MENSAJE = b'\x0C'
ANUNCIO_MENSAJE = b'\x0D'


class MensajeSistema(ABC):
    @abstractmethod
    def aBytes(self) -> bytes:
        pass

    @abstractmethod
    def deBytes(self, bytes: bytes) -> None:
        pass


class FinMensajeSistema(MensajeSistema):
    def __init__(self, clienteId: uuid.UUID = None, totalMsg: int = 1) -> None:
        self.clienteId = clienteId
        self.totalMsg = totalMsg    

    def aBytes(self) -> bytes:
        mensajeBytes = FIN_MENSAJE
        mensajeBytes += self.totalMsg.to_bytes(4, byteorder="big")
        mensajeBytes += self.clienteId.bytes
        return mensajeBytes
    

    def deBytes(self, bytes):
        self.totalMsg = int.from_bytes(bytes[0:4], byteorder="big")
        self.clienteId = uuid.UUID(bytes = bytes[4:20])


class AnuncioMensajeSistema(MensajeSistema):
    def __init__(self, clienteId: uuid.UUID = None, secuencias: list[int] = None) -> None:
        self.clienteId = clienteId
        self.secuencias = secuencias

    def aBytes(self) -> bytes:
        mensajeBytes = ANUNCIO_MENSAJE
        mensajeBytes += self.clienteId.bytes
        mensajeBytes += len(self.secuencias).to_bytes(4, byteorder="big")
        for secuencia in self.secuencias:
            mensajeBytes += secuencia.to_bytes(4, byteorder="big")
        return mensajeBytes

    def deBytes(self, bytes: bytes) -> None:
        self.clienteId = uuid.UUID(bytes=bytes[0:16])
        cantidad = int.from_bytes(bytes[16:20], byteorder="big")
        self.secuencias = [int.from_bytes(bytes[20+i*4:24+i*4], byteorder="big") for i in range(cantidad)]


class LoteDataMensajeSistema(MensajeSistema):
    def __init__(self, clienteId: uuid.UUID = None, lote: list[DataMensaje] = None, secuencia: int = 0) -> None:
        self.clienteId = clienteId
        self.lote = lote
        self.secuencia = secuencia


    def aBytes(self) -> bytes:
        bytesMensaje = LOTE_DATA_MENSAJE
        bytesMensaje += self.secuencia.to_bytes(4,byteorder="big")
        bytesMensaje += len(self.lote).to_bytes(2, byteorder="big")
        bytesMensaje += self.clienteId.bytes

        dataMensajeBytes = b''
        for mensaje in self.lote:
            dataMensajeBytes += mensaje.aBytes()
        
        bytesMensaje += dataMensajeBytes

        return bytesMensaje


    def deBytes(self, bytes: bytes) -> None:
        self.secuencia = int.from_bytes(bytes[0:4],byteorder="big")
        loteLen = int.from_bytes(bytes[4:6], byteorder="big")
        self.clienteId = uuid.UUID(bytes=(bytes[6:22]))
        totalLeido = 22

        self.lote = []
        for _ in range(loteLen):
            tamañoMensaje = int.from_bytes(bytes[totalLeido+1:totalLeido+5], byteorder="big")
            msg = DataMensaje()
            msg.deBytes(bytes[totalLeido+5:totalLeido+tamañoMensaje+5])
            self.lote.append(msg)
            totalLeido += tamañoMensaje + 5


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
        bytesMensaje += len(imgUrlBytes).to_bytes(4, byteorder="big")
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


class ImgLoteMensajeSistema(MensajeSistema):
    def __init__(self, clienteId: uuid.UUID = None, mensajes: list[ImgMensajeSistema] = None, secuencia: int = 0) -> None:
        self.clienteId = clienteId
        self.mensajes = mensajes
        self.secuencia = secuencia

    def aBytes(self) -> bytes:
        mensajeBytes = LOTE_IMG_MENSAJE
        mensajeBytes += self.secuencia.to_bytes(4, byteorder="big")
        mensajeBytes += self.clienteId.bytes
        mensajeBytes += len(self.mensajes).to_bytes(4, byteorder="big")

        for mensaje in self.mensajes:
            imgBytes = mensaje.aBytes()[1:]
            mensajeBytes += len(imgBytes).to_bytes(4, byteorder="big")
            mensajeBytes += imgBytes

        return mensajeBytes

    def deBytes(self, bytes: bytes) -> None:
        self.secuencia = int.from_bytes(bytes[0:4], byteorder="big")
        self.clienteId = uuid.UUID(bytes=(bytes[4:20]))
        total = int.from_bytes(bytes[20:24], byteorder="big")
        totalLeido = 24

        self.mensajes = []
        for _ in range(total):
            largo = int.from_bytes(bytes[totalLeido:totalLeido+4], byteorder="big")

            img = ImgMensajeSistema()
            img.deBytes(bytes[totalLeido+4:totalLeido+largo+4])

            self.mensajes.append(img)

            totalLeido += (largo + 4)


class TransformadorLoteMensajeSistema(MensajeSistema):
    def __init__(self, clienteId: uuid.UUID = None, mensajes: list = None, secuencia: int = 0) -> None:
        self.clienteId = clienteId
        self.mensajes = mensajes
        self.secuencia = secuencia

    def aBytes(self) -> bytes:
        mensajeBytes = LOTE_TRANFORMADOR_MENSAJE
        mensajeBytes += self.secuencia.to_bytes(4, byteorder="big")

        mensajeBytes += len(self.mensajes).to_bytes(4, byteorder="big")

        for mensaje in self.mensajes:
            transformadorBytes = mensaje.aBytes()
            mensajeBytes += len(transformadorBytes).to_bytes(4, byteorder="big")
            mensajeBytes += transformadorBytes

        mensajeBytes += self.clienteId.bytes
        
        return mensajeBytes

    def deBytes(self, bytes: bytes) -> None:
        self.secuencia = int.from_bytes(bytes[0:4], byteorder="big")
        totalLeido = 4

        total = int.from_bytes(bytes[totalLeido:totalLeido+4], byteorder="big")
        totalLeido += 4

        self.mensajes = []
        for _ in range(total):
            largo = int.from_bytes(bytes[totalLeido:totalLeido+4], byteorder="big")

            transformador = TransformadorMensajeSistema()
            transformador.deBytes(bytes[totalLeido+4:totalLeido+largo+4])

            self.mensajes.append(transformador)

            totalLeido += (largo + 4)

        self.clienteId = uuid.UUID(bytes=(bytes[totalLeido:totalLeido+16]))


class TransformadorMensajeSistema(MensajeSistema):
    def __init__(self, url: str = None, fecha: int = None, resumen: str = None, lenguaje: int = None ):
        self.url = url
        self.fecha = fecha
        self.resumen = resumen
        self.lenguaje = lenguaje


    def aBytes(self) -> bytes:
        urlBytes = self.url.encode("UTF-8")
        bytesMensaje = len(urlBytes).to_bytes(4, byteorder="big")
        bytesMensaje += urlBytes

        bytesMensaje += self.fecha.to_bytes(2, byteorder="big")

        resumenBytes = self.resumen.encode("UTF-8")
        bytesMensaje += len(resumenBytes).to_bytes(4, byteorder="big")
        bytesMensaje += resumenBytes

        bytesMensaje += self.lenguaje.to_bytes(2, byteorder="big")

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


class PalabrasLoteMensajeSistema(MensajeSistema):
    def __init__(self, clienteId: uuid.UUID = None, mensajes: list = None, secuencia: int = 0) -> None:
        self.clienteId = clienteId
        self.mensajes = mensajes
        self.secuencia = secuencia

    def aBytes(self) -> bytes:
        bytesMensaje = LOTE_PALABRAS_MENSAJE
        bytesMensaje += self.secuencia.to_bytes(4, byteorder="big")

        bytesMensaje += len(self.mensajes).to_bytes(4, byteorder="big")

        for mensaje in self.mensajes:
            palabrasBytes = mensaje.aBytes()
            bytesMensaje += len(palabrasBytes).to_bytes(4, byteorder="big")
            bytesMensaje += palabrasBytes

        bytesMensaje += self.clienteId.bytes

        return bytesMensaje


    def deBytes(self, bytes: bytes) -> None:
        self.secuencia = int.from_bytes(bytes[0:4], byteorder="big")
        totalLeido = 4

        total = int.from_bytes(bytes[totalLeido:totalLeido+4], byteorder="big")
        totalLeido += 4

        self.mensajes = []
        for _ in range(total):
            largo = int.from_bytes(bytes[totalLeido:totalLeido+4], byteorder="big")

            palabras = PalabrasMensajeSistema()
            palabras.deBytes(bytes[totalLeido+4:totalLeido+largo+4])

            self.mensajes.append(palabras)

            totalLeido += (largo + 4)

        self.clienteId = uuid.UUID(bytes=(bytes[totalLeido:totalLeido+16]))


class PalabrasMensajeSistema(MensajeSistema):
    def __init__(self, url: str = None, lenguaje: int = None, palabras: dict[str,int] = None) -> None:
        self.url = url
        self.lenguaje = lenguaje
        self.palabras = palabras

    
    def aBytes(self) -> bytes:
        urlBytes = self.url.encode("UTF-8")
        mensajeBytes = len(urlBytes).to_bytes(4, byteorder="big")
        mensajeBytes += urlBytes

        mensajeBytes += self.lenguaje.to_bytes(2, byteorder="big")

        palabraTotal = []
        for clave, valor in self.palabras.items():
            palabraTotal.append(clave)
            palabraTotal.append(str(valor)) 

        palabrasBytes = ",".join(palabraTotal).encode("UTF-8")
        mensajeBytes += len(palabrasBytes).to_bytes(4, byteorder="big")
        mensajeBytes += palabrasBytes

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


class CantidadPalabrasLoteMensajeSistema(MensajeSistema):
    def __init__(self, clienteId: uuid.UUID = None, mensajes: list = None, secuencia: int = 0):
        self.clienteId = clienteId
        self.mensajes = mensajes
        self.secuencia = secuencia

    def aBytes(self) -> bytes:
            mensajeBytes = LOTE_CANTIDAD_PALABRAS_MENSAJE
            mensajeBytes += self.secuencia.to_bytes(4, byteorder="big")

            mensajeBytes += len(self.mensajes).to_bytes(4, byteorder="big")
    
            for mensaje in self.mensajes:
                palabrasBytes = mensaje.aBytes()
                mensajeBytes += len(palabrasBytes).to_bytes(4, byteorder="big")
                mensajeBytes += palabrasBytes
    
            mensajeBytes += self.clienteId.bytes
            
            return mensajeBytes
    
    def deBytes(self, bytes: bytes) -> None:
        self.secuencia = int.from_bytes(bytes[0:4], byteorder="big")
        totalLeido = 4

        total = int.from_bytes(bytes[totalLeido:totalLeido+4], byteorder="big")
        totalLeido += 4
        
        self.mensajes = []
        for _ in range(total):
            largo = int.from_bytes(bytes[totalLeido:totalLeido+4], byteorder="big")
            palabras = CantidadPalabraMensajeSistema()
            palabras.deBytes(bytes[totalLeido+4:totalLeido+largo+4])
            
            self.mensajes.append(palabras)
            totalLeido += (largo + 4)
        
        self.clienteId = uuid.UUID(bytes=(bytes[totalLeido:totalLeido+16]))
    

class CantidadPalabraMensajeSistema(MensajeSistema):
    def __init__(self, url: str = None, cantidad : int = None) -> None:
        self.url = url
        self.cantidad = cantidad

    
    def aBytes(self) -> bytes:

        urlBytes = self.url.encode("UTF-8")
        mensajeBytes = len(urlBytes).to_bytes(4, byteorder="big")
        mensajeBytes += urlBytes

        mensajeBytes += self.cantidad.to_bytes(4, byteorder="big")

        return mensajeBytes
    

    def deBytes(self, bytes: bytes) -> None:
        totalLeido = 0

        urlLen = int.from_bytes(bytes[totalLeido:totalLeido+4], byteorder="big")
        self.url = bytes[totalLeido+4:totalLeido+urlLen+4].decode()
        totalLeido += (urlLen + 4)

        self.cantidad = int.from_bytes( bytes[totalLeido:totalLeido+4], byteorder="big")
        totalLeido += 4


class FinPromMensajeSistema(MensajeSistema):
    def __init__(self, clienteId: uuid.UUID = None, promedio: int = None, totalMsg: int = 0):
        self.clienteId = clienteId
        self.promedio = promedio
        self.totalMsg = totalMsg


    def aBytes(self) -> bytes:
        bytesMensaje = FIN_PROM_MENSAJE

        bytesMensaje += self.promedio.to_bytes(4, byteorder="big")
        bytesMensaje += self.totalMsg.to_bytes(4, byteorder="big")

        bytesMensaje += self.clienteId.bytes

        return bytesMensaje


    def deBytes(self, bytes: bytes) -> None:

        self.promedio = int.from_bytes(bytes[0:4], byteorder="big")
        self.totalMsg = int.from_bytes(bytes[4:8], byteorder="big")
        totalLeido = 8

        self.clienteId = uuid.UUID(bytes=bytes[totalLeido:totalLeido+16])


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
    def __init__(self, clienteId: uuid.UUID = None, palabras: list[str] = None):
        self.clienteId = clienteId
        self.palabras = palabras
    
    def aBytes(self) -> bytes:
        bytes_mensaje = RESPUESTA3_MENSAJE
        palabras_bytes = ",".join(self.palabras).encode("UTF-8")
        bytes_mensaje += len(palabras_bytes).to_bytes(4,byteorder="big")
        bytes_mensaje += palabras_bytes
        bytes_mensaje += self.clienteId.bytes

        return bytes_mensaje
    

    def deBytes(self, bytes) -> None:
        palabras_len = int.from_bytes(bytes[0:4],byteorder="big")
        offset_len_palabras = 4 + palabras_len
        self.palabras = bytes[4:offset_len_palabras].decode().split(",")

        offset_id_inicio = 4 + palabras_len
        offset_id_fin = offset_id_inicio + 16
        self.clienteId = uuid.UUID(bytes=bytes[offset_id_inicio:offset_id_fin])


    def aRespuestaGateway(self) -> Respuesta3Mensaje:
        return Respuesta3Mensaje(self.palabras)


class Respuesta4MensajeSistema(MensajeSistema):
    def __init__(self, clienteId: uuid.UUID = None, palabras: dict[str, int] = None):
        self.clienteId = clienteId
        self.palabras = palabras

    def aBytes(self) -> bytes:
        mensajeBytes = RESPUESTA4_MENSAJE

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


    def aRespuestaGateway(self) -> Respuesta4Mensaje:
        return Respuesta4Mensaje(self.palabras)


class Respuesta5MensajeSistema(MensajeSistema):
    def __init__(self, clienteId: uuid.UUID = None, data: dict[str, int] = None):
        self.clienteId  = clienteId
        self.data = data

    
    def aBytes(self) -> bytes:
        bytesMensaje = RESPUESTA5_MENSAJE
        bytesMensaje += (Respuesta5Mensaje(self.data).aBytes())[1:]
        bytesMensaje += self.clienteId.bytes

        return bytesMensaje
    

    def deBytes(self, bytes) -> None:
        rtamsg = Respuesta5Mensaje()
        rtamsg.deBytes(bytes[4:len(bytes)-16])
        self.data = rtamsg.data
        self.clienteId = uuid.UUID(bytes=bytes[len(bytes)-16:])


    def aRespuestaGateway(self) -> Respuesta5Mensaje:
        return Respuesta5Mensaje(self.data)


def recvMensajeSistema(mensaje: bytes) -> MensajeSistema:
    type = mensaje[:1]
    rta = None
    
    if type == FIN_MENSAJE:
        rta = FinMensajeSistema()
    elif type == LOTE_DATA_MENSAJE:
        rta = LoteDataMensajeSistema()
    elif type == LOTE_TRANFORMADOR_MENSAJE:
        rta = TransformadorLoteMensajeSistema()
    elif type == LOTE_PALABRAS_MENSAJE:
        rta = PalabrasLoteMensajeSistema()
    elif type == LOTE_CANTIDAD_PALABRAS_MENSAJE:
        rta = CantidadPalabrasLoteMensajeSistema()
    elif type == IMG_MENSAJE:
        rta = ImgMensajeSistema()
    elif type == LOTE_IMG_MENSAJE:
        rta = ImgLoteMensajeSistema()
    elif type == ANUNCIO_MENSAJE:
        rta = AnuncioMensajeSistema()
    elif type == FIN_PROM_MENSAJE:
        rta = FinPromMensajeSistema()
    elif type == RESPUESTA1_MENSAJE:
        rta = Respuesta1MensajeSistema() 
    elif type == RESPUESTA2_MENSAJE:
        rta = Respuesta2MensajeSistema()
    elif type == RESPUESTA3_MENSAJE:
        rta = Respuesta3MensajeSistema()
    elif type == RESPUESTA4_MENSAJE:
        rta = Respuesta4MensajeSistema()
    elif type == RESPUESTA5_MENSAJE:
        rta = Respuesta5MensajeSistema()
    else:
        rta = None
    
    if rta is None:
        return None
    else:
        rta.deBytes(mensaje[1:])
        return rta
