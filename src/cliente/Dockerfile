#FROM python:3-alpine (depende la pc me anda este o el otro xd)
FROM python:3.13-slim-bookworm

WORKDIR /home/app

COPY cliente/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY socket/safeSocket.py .
COPY protocolo/*.py .
COPY cliente .

ENTRYPOINT ["python3", "main.py"]