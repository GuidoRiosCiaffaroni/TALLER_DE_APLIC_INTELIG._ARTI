#!/bin/bash

# ==============================================================================
# SCRIPT DE INSTALACIÓN AUTOMÁTICA Y LIMPIA DE PGADMIN 4 (MODO WEB)
# ==============================================================================
# Notas: Ejecutar como root o con sudo.
# ==============================================================================

# --- CONFIGURACIÓN ---
# Define las credenciales que usarás para iniciar sesión en la interfaz Web
PGADMIN_EMAIL="admin@tudominio.com"   # Puedes cambiarlo por tu correo
PGADMIN_PASS="ClaveWebPgAdmin4"        # Cambia esto por una contraseña segura

# Salir inmediatamente si algún comando falla
set -e

echo "=== [1/5] Limpiando residuos anteriores de repositorios ==="
sudo rm -f /etc/apt/sources.list.d/pgadmin4.list

echo "=== [2/5] Añadiendo el repositorio oficial de pgAdmin 4 ==="
# Instalar dependencias iniciales
sudo apt-get update && sudo apt-get install -y curl gnupg2 lsb-release

# Importar la llave GPG oficial de pgAdmin
sudo curl -fsS https://www.pgadmin.org/static/packages_pgadmin_org.pub | sudo gpg --dearmor --yes -o /usr/share/keyrings/pgadmin-archive-keyring.gpg

# Añadir el repositorio oficial adaptado a tu versión de Ubuntu
echo "deb [signed-by=/usr/share/keyrings/pgadmin-archive-keyring.gpg] https://ftp.postgresql.org/pub/pgadmin/pgadmin4/apt/$(lsb_release -cs) pgadmin4 main" | sudo tee /etc/apt/sources.list.d/pgadmin4.list

echo "=== [3/5] Instalando dependencias de Python para pgAdmin ==="
sudo apt-get update
# Forzamos la instalación del entorno de Python del sistema para evitar errores de Flask
sudo apt-get install -y python3-pgadmin4

echo "=== [4/5] Instalando pgAdmin 4 (Versión Web) ==="
sudo apt-get install -y pgadmin4-web

echo "=== [5/5] Configurando el servidor web Apache para pgAdmin ==="
# Exportamos las variables para que el configurador oficial de pgAdmin las tome automáticamente
export PGADMIN4_SETUP_EMAIL="${PGADMIN_EMAIL}"
export PGADMIN4_SETUP_PASSWORD="${PGADMIN_PASS}"

# Ejecuta el script oficial en modo desatendido (sin preguntar en terminal)
sudo /usr/pgadmin4/bin/pgadmin4-web-setup.sh --no-prompt

echo "=============================================================================="
echo " ¡pgAdmin 4 se ha instalado y configurado correctamente! "
echo "=============================================================================="
echo " Acceso Web en tu navegador:"
echo "   URL:        http://localhost/pgadmin4  o  http://IP_DE_TU_SERVIDOR/pgadmin4"
echo "   Usuario:    ${PGADMIN_EMAIL}"
echo "   Contraseña: ${PGADMIN_PASS}"
echo "=============================================================================="