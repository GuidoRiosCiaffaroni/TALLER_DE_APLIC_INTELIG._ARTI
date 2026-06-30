#!/bin/bash

# ==============================================================================
# SCRIPT DE INSTALACIÓN AUTOMÁTICA DE POSTGRESQL EN UBUNTU
# ==============================================================================
# Notas: Ejecutar como root o con sudo.
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
# Importar la llave GPG oficial
install -d /etc/apt/keyrings
curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo gpg --dearmor -o /etc/apt/keyrings/postgresql.gpg

# Añadir el repositorio a las fuentes de APT
echo "deb [signed-by=/etc/apt/keyrings/postgresql.gpg] http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" | sudo tee /etc/apt/sources.list.d/pgdg.list

echo "=== [4/5] Instalando PostgreSQL ${PG_VERSION} y componentes esenciales ==="
sudo apt-get update
sudo apt-get install -y postgresql-${PG_VERSION} postgresql-contrib-${PG_VERSION}

echo "=== [5/5] Verificando y habilitando el servicio ==="
sudo systemctl daemon-reload
sudo systemctl enable postgresql
sudo systemctl start postgresql

# --- CONFIGURACIÓN DE FIREWALL (OPCIONAL) ---
# Si necesitas acceso remoto, descomenta las siguientes líneas para abrir el puerto 5432
# echo "=== [EXTRA] Configurando UFW para permitir tráfico en el puerto 5432 ==="
# sudo ufw allow 5432/tcp

echo "=============================================================================="
echo " ¡PostgreSQL ${PG_VERSION} se ha instalado y está corriendo exitosamente! "
echo "=============================================================================="
sudo systemctl status postgresql --no-pager