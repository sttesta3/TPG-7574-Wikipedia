FROM nodo-base

COPY imgDescargador/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY imgDescargador .

ENTRYPOINT ["python3", "main.py"]