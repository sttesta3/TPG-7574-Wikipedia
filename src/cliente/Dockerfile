FROM python:3-alpine

WORKDIR /home/app

COPY cliente/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY socket/safeSocket.py .
COPY protocolo/*.py .
COPY cliente .

ENTRYPOINT ["python3", "main.py"]