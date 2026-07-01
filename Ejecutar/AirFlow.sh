#!/bin/bash

# 1. Navegar a la carpeta del proyecto
cd /root/airflow_project

# 2. Activar el entorno usando el punto (.) para compatibilidad universal
. airflow_env/bin/activate

# 3. Declarar la ruta de configuración
export AIRFLOW_HOME=/root/airflow_project/airflow

# 4. Levantar los servicios
airflow webserver -p 8080 &
airflow scheduler