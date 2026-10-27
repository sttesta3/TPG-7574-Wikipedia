FROM python:3-alpine

WORKDIR /home/app

COPY clasificador/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY protocolo/*.py .
COPY socket/safeSocket.py .
COPY middleware/middleware.py .
COPY clienteLock/clienteLock.py .
COPY clasificador .

ENTRYPOINT ["python3", "main.py"]