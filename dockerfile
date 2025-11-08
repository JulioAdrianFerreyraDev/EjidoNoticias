# Usar una imagen base de Python
FROM python:3.11-slim

# Establecer variables de entorno para Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalar dependencias
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copiar el resto del código del proyecto
COPY . .