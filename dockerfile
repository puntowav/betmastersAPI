FROM python:3.10-slim

# Instala los paquetes de sistema necesarios para compilar mariadb
RUN apt-get update && apt-get install -y libmariadb-dev gcc

# Expone el puerto 443
EXPOSE 443

WORKDIR /app

# Copia el requirements.txt
COPY API/requirements.txt /app/requirements.txt

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el código de la carpeta API
COPY API /app/

# Arranca uvicorn con SSL
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "443", "--ssl-keyfile", "/app/ssl/key.pem", "--ssl-certfile", "/app/ssl/cert.pem"]