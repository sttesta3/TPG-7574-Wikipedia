FROM python:3-alpine

WORKDIR /home/app

COPY gateway/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY utils/socket/safeSocket.py .
COPY utils/protocolo/*.py protocolo/
COPY utils/middleware/middleware.py .
COPY gateway .

ENTRYPOINT ["python3", "main.py"]