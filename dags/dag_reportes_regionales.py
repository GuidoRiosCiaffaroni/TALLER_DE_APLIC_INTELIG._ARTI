from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator

# Ruta base donde se encuentra su estructura en el servidor Linux
# ¡Cambie esto por la ruta absoluta real de su servidor! (Ej: /home/usuario/proyecto)
RUTA_BASE = "/ruta/absoluta/a/su/proyecto"

default_args = {
    'owner': 'Profesor_Airflow',
    'depends_on_past': False,
    'start_date': datetime(2026, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=3),
}

with DAG(
    dag_id='ejecucion_individual_scripts',
    default_args=default_args,
    description='Orquestando la estructura de archivos local de forma individual',
    schedule_interval=None, # Lo dejamos manual para que pruebe uno a uno
    catchup=False,
    tags=['linux', 'produccion'],
) as dag:

    # 1. Tarea para ejecutar el script de subida/carga en la raíz
    tarea_upload = BashOperator(
        task_id='ejecutar_upload_sh',
        bash_command=f'cd {RUTA_BASE} && ./upload.sh',
    )

    # 2. Tareas individuales para la carpeta 'script'
    tarea_reporte_banco_mundial = BashOperator(
        task_id='reporte_banco_mundial',
        bash_command=f'python3 {RUTA_BASE}/script/reporte_banco_mundial.py',
    )

    tarea_reporte_cepal = BashOperator(
        task_id='reporte_cepal_linux',
        bash_command=f'python3 {RUTA_BASE}/script/reporte_cepal_linux.py',
    )

    tarea_reporte_chile = BashOperator(
        task_id='reporte_chile_abierto',
        bash_command=f'python3 {RUTA_BASE}/script/reporte_chile_abierto.py',
    )

    # 3. Definición de dependencias
    # Imaginemos que primero requerimos subir/preparar datos con upload.sh 
    # y luego podemos correr los tres reportes en paralelo de forma independiente
    tarea_upload >> [tarea_reporte_banco_mundial, tarea_reporte_cepal, tarea_reporte_chile]