from pathlib import Path
import pandas as pd

def procesar_datos_banco_mundial():
    # 1. Configurar las rutas relativas usando pathlib
    # __file__ es la ubicación de este script (tu_proyecto/script/procesar_datos.py)
    script_dir = Path(__file__).resolve().parent
    
    # Subimos un nivel (raíz) y entramos a la carpeta 'Data'
    data_dir = script_dir.parent / "Data"
    
    # Definir rutas exactas de entrada y salida
    ruta_entrada = data_dir / "datos_bancomundial_chl_1960_2026.csv"
    ruta_salida = data_dir / "datos_bancomundial_procesados.csv"

    # 2. Verificar que el archivo de origen realmente exista en 'Data'
    if not ruta_entrada.exists():
        print(f"Error: No se encontró el archivo de origen en: {ruta_entrada}")
        print("Asegúrate de que la carpeta 'Data' y el archivo existan en la raíz del proyecto.")
        return

    print(f"Cargando datos desde: {ruta_entrada}")
    df = pd.read_csv(ruta_entrada)
    print(f"Registros a procesar: {len(df)}")

    # TAREA 1: Agregar columna ID al principio (empezando en 1)
    df.insert(0, 'ID', range(1, len(df) + 1))
    
    # TAREA 2: Agregar columna 'origen' con el valor 'WB'
    df['origen'] = 'WB'

    # 3. Asegurar que la carpeta 'Data' exista antes de guardar (por seguridad)
    data_dir.mkdir(parents=True, exist_ok=True)

    # 4. Guardar el archivo resultante en la carpeta 'Data'
    print(f"Guardando archivo procesado en: {ruta_salida}")
    df.to_csv(ruta_salida, index=False)
    print("¡Pipeline de datos ejecutado con éxito!")

if __name__ == "__main__":
    procesar_datos_banco_mundial()