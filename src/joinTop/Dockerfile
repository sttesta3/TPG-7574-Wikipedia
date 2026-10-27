FROM python:3-alpine

WORKDIR /home/app

COPY joinTop/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY socket/safeSocket.py .
COPY protocolo/*.py .
COPY middleware/middleware.py .
COPY joinTop .

ENTRYPOINT ["python3", "main.py"]