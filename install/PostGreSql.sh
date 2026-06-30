#!/bin/bash

# ==============================================================================
# SCRIPT DE INSTALACIÓN AUTOMÁTICA DE POSTGRESQL (CON AUTOLIMPIEZA PREVIA)
# ==============================================================================
# Ejecutar como root o con sudo.
# ==============================================================================

# Salir inmediatamente si un comando falla de manera inesperada
set -e

echo "=== [0/4] Fase de Limpieza Previa ==="
echo "Eliminando repositorios externos antiguos si existen..."
sudo rm -f /etc/apt/sources.list.d/pgdg.list

echo "Limpiando la caché local de paquetes rotos..."
sudo apt-get clean
sudo apt-get autoremove -y

echo "=== [1/4] Actualizando las listas de paquetes nativos ==="
sudo apt-get update

echo "=== [2/4] Instalando PostgreSQL nativo y componentes esenciales ==="
# Instalamos la versión nativa soportada por el sistema para evitar conflictos con libicu
sudo apt-get install -y postgresql postgresql-contrib

echo "=== [3/4] Verificando y habilitando el servicio ==="
sudo systemctl daemon-reload
sudo systemctl enable postgresql
sudo systemctl start postgresql

echo "=============================================================================="
echo "   ¡PostgreSQL se ha purgado, instalado y activado exitosamente!              "
echo "=============================================================================="
sudo systemctl status postgresql --no-pager