#!/bin/sh
set -e

echo "Aguardando o banco de dados..."

while ! nc -z db 5432; do
  sleep 1
done

echo "Banco de dados pronto!"

echo "Executando o script de preenchimento do banco de dados..."
python -m app.scripts.seed_data

echo "Iniciando a API..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
