FROM python:3-alpine

WORKDIR /home/app

COPY sumTop/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN python -m nltk.downloader -d /usr/local/share/nltk_data stopwords

COPY socket/safeSocket.py .
COPY protocolo/*.py .
COPY middleware/middleware.py .
COPY sumTop .

ENTRYPOINT ["python3", "main.py"]