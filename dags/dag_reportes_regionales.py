from datetime import datetime, timedelta
from airflow import DAG
# Importación clásica y compatible con todas las versiones de Airflow 2.x
from airflow.operators.bash import BashOperator

# Definimos la ruta donde están guardados sus scripts en el servidor
RUTA_BASE = "/root/airflow_project"

default_args = {
    'owner': 'Profesor_Airflow',
    'depends_on_past': False,
    'start_date': datetime(2026, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=3),
}

with DAG(
    dag_id='orquestador_scripts_individuales',
    default_args=default_args,
    description='Mapeo de archivos de reportes en Linux',
    schedule_interval=None,  # Manual para ejecución individual
    catchup=False,
    tags=['reportes', 'linux'],
) as dag:

    upload_sh = BashOperator(
        task_id='1_ejecutar_upload_sh',
        bash_command=f'cd {RUTA_BASE} && ./upload.sh',
    )

    banco_mundial = BashOperator(
        task_id='2_reporte_banco_mundial',
        bash_command=f'python3 {RUTA_BASE}/script/reporte_banco_mundial.py',
    )

    cepal = BashOperator(
        task_id='3_reporte_cepal_linux',
        bash_command=f'python3 {RUTA_BASE}/script/reporte_cepal_linux.py',
    )

    chile_abierto = BashOperator(
        task_id='4_reporte_chile_abierto',
        bash_command=f'python3 {RUTA_BASE}/script/reporte_chile_abierto.py',
    )

    # Flujo de tareas secuencial o en paralelo
    upload_sh >> [banco_mundial, cepal, chile_abierto]