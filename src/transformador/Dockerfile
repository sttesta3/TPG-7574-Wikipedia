FROM nodo-base:latest

COPY transformador/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m nltk.downloader -d /usr/local/share/nltk_data stopwords

COPY transformador .

ENTRYPOINT ["python3", "main.py"]