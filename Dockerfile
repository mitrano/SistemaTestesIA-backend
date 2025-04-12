# Usa uma imagem oficial do Python como base
FROM python:3.11-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos da aplicação para o container
COPY main.py /app/

# Copia o arquivo de requirements (vamos criar abaixo)
COPY requirements.txt /app/

# Instala dependências do sistema necessárias para o SQLite e para compilar pacotes Python
RUN apt-get update && apt-get install -y \
    gcc \
    libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*

# Instala as dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta padrão da FastAPI (caso rode com Uvicorn)
EXPOSE 8000

# Comando para iniciar a aplicação
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
