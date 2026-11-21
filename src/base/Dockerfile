FROM python:3-alpine

WORKDIR /home/app

RUN pip install --no-cache-dir pika==1.4.4

COPY utils/timer/timper.py timer.py
COPY utils/latido/latido.py latido.py
COPY utils/wal/wal.py wal.py
COPY utils/raft/raft.py raft.py
COPY utils/protocolo/ protocolo/
COPY utils/socket/safeSocket.py safeSocket.py
COPY utils/middleware/middleware.py middleware.py
COPY utils/contadorDistribuido/contadorDistribuido.py .