FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    nginx \
    python3 \
    python3-pip \
    python3-venv \
    ansible \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Crear directorios del proyecto
RUN mkdir -p /opt/ansible-visual/api \
    && mkdir -p /var/www/ansible-visual/html

# Crear entorno virtual de Python
RUN python3 -m venv /opt/ansible-visual/api/venv

# Instalar dependencias de Python en el entorno virtual
RUN /opt/ansible-visual/api/venv/bin/pip install --no-cache-dir fastapi uvicorn gunicorn

# Copiar configuración de Nginx
COPY nginx.conf /etc/nginx/sites-available/default

# Copiar archivos del frontend
COPY frontend/ /var/www/ansible-visual/html/

# Copiar archivos del backend
COPY api/ /opt/ansible-visual/api/

# Copiar script de inicio
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Exponer puerto 80 (Nginx)
EXPOSE 80

# Iniciar Nginx + Gunicorn
CMD ["/start.sh"]
