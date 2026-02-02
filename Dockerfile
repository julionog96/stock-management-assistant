FROM python:3.11-slim

WORKDIR /app

# netcat para o entrypoint aguardar o Postgres aceitar conexões
RUN apt-get update && apt-get install -y --no-install-recommends netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Garante que o entrypoint rode: esperar DB → seed → uvicorn
RUN chmod +x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
