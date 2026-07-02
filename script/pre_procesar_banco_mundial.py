from pathlib import Path
import pandas as pd

def ejecutar_pipeline_banco_mundial():
    # 1. Mapeo dinámico de rutas basado en la ubicación del script
    # __file__ obtiene la ruta de este archivo (ej. /tu_proyecto/script/procesar.py)
    script_dir = Path(__file__).resolve().parent
    
    # Navegamos un nivel arriba (raíz) y entramos a la carpeta hermana 'Data'
    data_dir = script_dir.parent / "Data"
    
    # Definición de rutas específicas de los archivos
    ruta_entrada = data_dir / "datos_bancomundial_chl_1960_2026.csv"
    ruta_salida = data_dir / "datos_bancomundial_procesados.csv"

    # 2. Control de excepciones: Validación de existencia del archivo origen
    if not ruta_entrada.exists():
        print(f"[ERROR] No se localizó el archivo origen en: {ruta_entrada}")
        print("Asegúrate de que el archivo CSV se encuentre dentro de la carpeta 'Data/'.")
        return

    print(f"[INFO] Iniciando lectura de datos desde: {ruta_entrada}")
    # Carga del dataset en un DataFrame de Pandas
    df = pd.read_csv(ruta_entrada)
    print(f"[INFO] Dataset cargado correctamente. Registros detectados: {len(df)}")

    # TAREA 1: Insertar la columna 'ID' correlativa al inicio (índice 0)
    # Genera una serie secuencial que va desde 1 hasta el total de filas
    df.insert(0, 'ID', range(1, len(df) + 1))
    
    # TAREA 2: Crear la columna 'origen' asignando el valor constante 'WB'
    df['origen'] = 'WB'

    # 3. Guardado defensivo: Asegura la persistencia en el directorio destino
    data_dir.mkdir(parents=True, exist_ok=True)

    # 4. Exportación final de los datos transformados
    print(f"[INFO] Exportando datos procesados a: {ruta_salida}")
    # index=False evita que Pandas escriba el índice implícito por defecto
    df.to_csv(ruta_salida, index=False)
    print("[ÉXITO] El proceso ha concluido de forma satisfactoria.")

if __name__ == "__main__":
    ejecutar_pipeline_banco_mundial()