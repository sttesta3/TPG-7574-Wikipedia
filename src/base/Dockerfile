FROM python:3-alpine

WORKDIR /home/app

RUN pip install --no-cache-dir pika==1.4.4

COPY utils/raft/ raft/
COPY utils/protocolo/ protocolo/
COPY utils/socket/safeSocket.py safeSocket.py
COPY utils/middleware/middleware.py middleware.py
COPY utils/contadorEof/contadorEof.py .