FROM python:3-alpine

WORKDIR /home/app

COPY gateway/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY socket/safeSocket.py .
COPY protocolo/mensajesCliente.py ./mensajesCliente.py
COPY protocolo/mensajesGateway.py ./mensajesGateway.py
COPY middleware/middleware.py .
COPY gateway .

ENTRYPOINT ["python3", "main.py"]