#!/bin/bash

# Detener el script si ocurre algún error
set -e

echo "=================================================="
echo " Airflow Installation with PostgreSQL Backend"
echo "=================================================="

# Credenciales NUEVAS que usará Airflow de forma interna
AIRFLOW_DB_USER="airflow_user"
AIRFLOW_DB_PASS="airflow_pass" 
AIRFLOW_DB_NAME="airflow_db"

# 1. Actualizar sistema e instalar dependencias de desarrollo para Postgres
echo "--> Installing system and postgres development dependencies..."
sudo apt update
sudo apt install python3 python3-pip python3-venv build-essential libssl-dev libffi-dev python3-dev libpq-dev -y

# 2. Crear la Base de Datos y el Usuario dedicado en tu Postgres de forma local
echo "--> Creating Airflow database and user in PostgreSQL..."
# Usamos el usuario 'postgres' nativo del sistema para obviar bloqueos de contraseñas de red TCP/IP
sudo -u postgres psql -c "CREATE USER $AIRFLOW_DB_USER WITH PASSWORD '$AIRFLOW_DB_PASS';" || echo "El usuario ya existe, continuando..."
sudo -u postgres psql -c "CREATE DATABASE $AIRFLOW_DB_NAME OWNER $AIRFLOW_DB_USER;" || echo "La base de datos ya existe, continuando..."

# 3. Estructurar el entorno virtual de Python
echo "--> Setting up Python virtual environment..."
PROJECT_DIR="$HOME/airflow_project"
mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR"

if [ ! -d "airflow_env" ]; then
    python3 -m venv airflow_env
fi

# Activación con el operador universal '.' para evitar el error 'source: not found'
. airflow_env/bin/activate

# 4. Configurar variables de entorno e instalar Airflow con el driver de postgres
echo "--> Installing Apache Airflow with Postgres provider..."
export AIRFLOW_HOME="$PROJECT_DIR/airflow"

pip install --upgrade pip
# Instalación directa para solucionar la falta de constraints en Python 3.13
pip install "apache-airflow[postgres]==2.10.2"

# 5. Generar la configuración e inyectar la cadena de conexión de Postgres
echo "--> Generating Airflow configuration..."
mkdir -p "$AIRFLOW_HOME"
mkdir -p "$AIRFLOW_HOME/dags"

# Cadena de conexión usando el usuario interno de Airflow
SQL_ALCHEMY_CONN="postgresql+psycopg2://${AIRFLOW_DB_USER}:${AIRFLOW_DB_PASS}@localhost:5432/${AIRFLOW_DB_NAME}"

# Inicializar Base de Datos aplicando la variable de entorno
export AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=$SQL_ALCHEMY_CONN
airflow db init

# Modificar el archivo físico airflow.cfg para que los cambios sean permanentes
sed -i "s|sql_alchemy_conn = .*|sql_alchemy_conn = ${SQL_ALCHEMY_CONN}|g" "$AIRFLOW_HOME/airflow.cfg"
# Cambiar el Executor a LocalExecutor para habilitar el paralelismo real de tareas
sed -i "s|executor = SequentialExecutor|executor = LocalExecutor|g" "$AIRFLOW_HOME/airflow.cfg"
# Desactivar los DAGs de ejemplo para mantener limpio el panel
sed -i 's/load_examples = True/load_examples = False/g' "$AIRFLOW_HOME/airflow.cfg"

# 6. Crear usuario Administrador para la interfaz Web de Airflow
echo "--> Creating Airflow Web Admin user..."
airflow users create \
    --username admin \
    --firstname Guido \
    --lastname Rios \
    --role Admin \
    --email admin@example.com \
    --password adminpass || echo "El usuario administrador web ya existe."

echo "=================================================="
echo " ¡Instalación Completada con Éxito!"
echo "=================================================="
echo " Puedes verificar la nueva estructura en tu pgAdmin (localhost/pgadmin4/):"
echo " - Base de datos creada: $AIRFLOW_DB_NAME"
echo "=================================================="
echo " Para iniciar Airflow ejecuta:"
echo " cd $PROJECT_DIR && source airflow_env/bin/activate"
echo " export AIRFLOW_HOME=$PROJECT_DIR/airflow"
echo " airflow webserver -p 8080 & airflow scheduler"
echo "=================================================="