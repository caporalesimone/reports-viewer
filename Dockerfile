# Usa un'immagine di base minimale con Python
FROM python:3.12.6-alpine

# Imposta la directory di lavoro nel container
WORKDIR /app

# Copia i file necessari per il progetto
COPY requirements.txt .
COPY server.py .
COPY templates/ ./templates

# Installa le dipendenze
RUN pip install --no-cache-dir -r requirements.txt

# Espone la porta 5000 nel container
EXPOSE 5000

# Comando di avvio del server
CMD ["python", "server.py"]
