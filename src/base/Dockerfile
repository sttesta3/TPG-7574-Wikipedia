FROM python:3-alpine

WORKDIR /home/app

RUN pip install --no-cache-dir pika==1.4.4

COPY protocolo/ protocolo/
COPY middleware/middleware.py middleware.py
COPY socket/safeSocket.py safeSocket.py
