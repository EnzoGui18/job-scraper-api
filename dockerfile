# Use a imagem oficial Python 3.9 slim
FROM python:3.9-slim

# Evitar problemas com interatividade durante a instalação
ENV DEBIAN_FRONTEND=noninteractive

# Instalar dependências do sistema e Chrome/Selenium
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        wget \
        gnupg \
        unzip \
        xvfb \
        chromium \
        chromium-driver \
        postgresql-client \
        netcat-openbsd \
        curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Configurar variáveis de ambiente
ENV CHROME_BIN=/usr/bin/chromium \
    CHROMEDRIVER_PATH=/usr/bin/chromedriver \
    DISPLAY=:99 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Criar e definir o diretório de trabalho
WORKDIR /app

# Copiar os arquivos de requisitos primeiro
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o resto do código
COPY . .

# Criar usuário não-root
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Expor a porta que o Flask usará
EXPOSE 5000

# Comando para iniciar a aplicação
CMD ["flask", "run", "--host=0.0.0.0"]