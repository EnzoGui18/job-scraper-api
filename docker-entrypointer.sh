#!/bin/bash
set -e

# Esperar o PostgreSQL estar pronto
echo "Waiting for PostgreSQL..."
while ! nc -z db 5432; do
    sleep 0.1
done
echo "PostgreSQL started"

# Aplicar migrações do banco de dados
echo "Applying database migrations..."
flask db upgrade

# Iniciar o Xvfb (X Virtual Framebuffer)
Xvfb :99 -screen 0 1280x1024x24 > /dev/null 2>&1 &

# Iniciar a aplicação Flask
echo "Starting Flask application..."
exec gunicorn --bind 0.0.0.0:5000 --workers 4 --threads 2 "run:app"