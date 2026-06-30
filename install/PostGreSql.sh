#!/bin/bash

# ==============================================================================
# SCRIPT DE INSTALACIÓN AUTOMÁTICA DE POSTGRESQL (CORREGIDO PARA UBUNTU RECIENTE)
# ==============================================================================

# --- CONFIGURACIÓN ---
# Define la versión de PostgreSQL que deseas instalar (ej. 14, 15, 16 o 17)
PG_VERSION="16"

# Salir inmediatamente si un comando falla
set -e

echo "=== [1/5] Actualizando el sistema operativo ==="
sudo apt-get update && sudo apt-get upgrade -y

echo "=== [2/5] Instalando dependencias necesarias ==="
sudo apt-get install -y gnupg2 wget ca-certificates lsb-release curl

echo "=== [3/5] Añadiendo el repositorio oficial de PostgreSQL ==="
# Asegurar la existencia del directorio de llaveros
sudo install -d /etc/apt/keyrings

# Importar la llave GPG oficial de PostgreSQL
curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo gpg --dearmor --yes -o /etc/apt/keyrings/postgresql.gpg

# CORRECCIÓN: Forzamos la rama 'noble' para evitar el error 404 de compatibilidad en entornos de desarrollo avanzados
echo "deb [signed-by=/etc/apt/keyrings/postgresql.gpg] http://apt.postgresql.org/pub/repos/apt noble-pgdg main" | sudo tee /etc/apt/sources.list.d/pgdg.list

echo "=== [4/5] Instalando PostgreSQL ${PG_VERSION} y componentes esenciales ==="
sudo apt-get update
sudo apt-get install -y postgresql-${PG_VERSION} postgresql-contrib-${PG_VERSION}

echo "=== [5/5] Verificando y habilitando el servicio ==="
sudo systemctl daemon-reload
sudo systemctl enable postgresql
sudo systemctl start postgresql

echo "=============================================================================="
echo " ¡PostgreSQL ${PG_VERSION} se ha instalado y está corriendo exitosamente! "
echo "=============================================================================="
sudo systemctl status postgresql --no-pager