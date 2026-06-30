#!/bin/bash

# ==============================================================================
# SCRIPT DE CONFIGURACIÓN DE USUARIO E INSTALACIÓN DE PGADMIN 4 WEB
# ==============================================================================
# Ejecutar como root o con sudo.
# ==============================================================================

# --- CONFIGURACIÓN ---
# Define los datos para el nuevo usuario administrador de PostgreSQL
DB_USER="admin_user"
DB_PASS="TuContrasenaSegura123" # ¡Cambia esto!

# Define las credenciales para iniciar sesión en la interfaz Web de pgAdmin
PGADMIN_EMAIL="admin@tudominio.com" # ¡Cambia esto!
PGADMIN_PASS="ClaveWebPgAdmin4"      # ¡Cambia esto!

set -e

echo "=== [1/4] Creando usuario administrador en PostgreSQL ==="
# Enviamos el comando SQL directamente al clúster local de Postgres
sudo -u postgres psql -c "CREATE USER ${DB_USER} WITH SUPERUSER PASSWORD '${DB_PASS}';"
echo "Usuario '${DB_USER}' creado exitosamente con privilegios de Superusuario."

echo "=== [2/4] Añadiendo el repositorio oficial de pgAdmin 4 ==="
# Instalar la llave pública del repositorio de pgAdmin
sudo curl -fsS https://www.pgadmin.org/static/packages_pgadmin_org.pub | sudo gpg --dearmor --yes -o /usr/share/keyrings/pgadmin-archive-keyring.gpg

# Añadir el repositorio a las fuentes de APT de forma genérica
echo "deb [signed-by=/usr/share/keyrings/pgadmin-archive-keyring.gpg] https://ftp.postgresql.org/pub/pgadmin/pgadmin4/apt/$(lsb_release -cs) pgadmin4 main" | sudo tee /etc/apt/sources.list.d/pgadmin4.list

echo "=== [3/4] Instalando pgAdmin 4 (Modo Web) ==="
sudo apt-get update
# Instalamos la versión exclusiva para entorno web (evita instalar dependencias gráficas de escritorio)
sudo apt-get install -y pgadmin4-web

echo "=== [4/4] Configurando el servidor Web para pgAdmin ==="
# El paquete incluye un script oficial de configuración automatizada para Apache. 
# Le pasamos las credenciales mediante variables de entorno para que no pida interacción por teclado.
export PGADMIN4_SETUP_EMAIL="${PGADMIN_EMAIL}"
export PGADMIN4_SETUP_PASSWORD="${PGADMIN_PASS}"

sudo /usr/test/pgadmin4/bin/pgadmin4-web-setup.sh --no-prompt

echo "=============================================================================="
echo " ¡Configuración completada con éxito! "
echo "=============================================================================="
echo " Puedes acceder a la interfaz web desde tu navegador en:"
echo " http://localhost/pgadmin4  o  http://TU_IP_SERVIDOR/pgadmin4"
echo ""
echo " Credenciales de acceso Web:"
echo "   - Usuario/Email: ${PGADMIN_EMAIL}"
echo "   - Contraseña:    ${PGADMIN_PASS}"
echo "------------------------------------------------------------------------------"
echo " Credenciales de conexión para PostgreSQL (dentro de pgAdmin):"
echo "   - Host:          localhost"
echo "   - Puerto:        5432"
echo "   - Usuario:       ${DB_USER}"
echo "   - Contraseña:    ${DB_PASS}"
echo "=============================================================================="