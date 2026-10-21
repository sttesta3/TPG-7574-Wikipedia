FROM python:3-alpine

WORKDIR /home/app

COPY cuentaProm/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY socket/safeSocket.py .
COPY protocolo/*.py .
COPY middleware/middleware.py .
COPY cuentaProm .

ENTRYPOINT ["python3", "main.py"]