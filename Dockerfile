FROM python:3.12-slim

# Instalar dependencias esenciales del sistema operativo
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Establecer el directorio de trabajo idéntico a tu ruta local
WORKDIR /home/gonsa/mi_proyecto_mining

# Copiar el archivo de dependencias e instalarlas todas de un golpe
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código fuente del proyecto al contenedor
COPY . .

# Exponer el puerto por donde transmite el Dashboard
EXPOSE 8050

# COMANDO MAESTRO: Ejecuta el flujo de Prefect (Ingesta + dbt) y luego levanta el Dashboard
CMD ["sh", "-c", "python3 scripts/main_flow.py && python3 scripts/dashboard.py"]
