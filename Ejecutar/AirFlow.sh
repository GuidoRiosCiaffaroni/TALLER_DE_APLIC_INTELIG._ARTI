# 1. Navegar a la carpeta del proyecto
cd /root/airflow_project

# 2. Activar el entorno virtual de Python
source airflow_env/bin/activate

# 3. Informar a Airflow dónde leer las configuraciones
export AIRFLOW_HOME=/root/airflow_project/airflow

# 4. Levantar el Webserver en segundo plano (así liberas la consola)
airflow webserver -p 8080 &

# 5. Levantar el Scheduler (este se quedará mostrando logs en tiempo real)
airflow scheduler