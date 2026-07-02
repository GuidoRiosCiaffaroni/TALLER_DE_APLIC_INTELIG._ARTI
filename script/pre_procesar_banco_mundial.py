from pathlib import Path
import pandas as pd

def procesar_datos_banco_mundial():
    # Anclaje dinámico: detecta la ubicación exacta de este script
    script_dir = Path(__file__).resolve().parent
    
    # Sube un nivel a la raíz y entra a 'Data'
    data_dir = script_dir.parent / "Data"
    
    # Definición de archivos usando rutas absolutas calculadas
    ruta_entrada = data_dir / "datos_bancomundial_chl_1960_2026.csv"
    ruta_salida = data_dir / "datos_bancomundial_procesados.csv"

    # Validación defensiva de existencia
    if not ruta_entrada.exists():
        print(f"[ERROR] No se encontró el archivo en:\n --> {ruta_entrada}")
        return

    print(f"[PROCESO] Cargando: {ruta_entrada.name}")
    df = pd.read_csv(ruta_entrada)
    
    # TAREA 1: Columna ID secuencial al inicio (columna 0)
    df.insert(0, 'ID', range(1, len(df) + 1))
    
    # TAREA 2: Columna origen con valor "WB"
    df['origen'] = 'WB'

    # Guardar los cambios directamente en la carpeta Data
    print(f"[PROCESO] Guardando: {ruta_salida.name}")
    df.to_csv(ruta_salida, index=False)
    print("[ÉXITO] Archivo procesado y almacenado correctamente.")

if __name__ == "__main__":
    procesar_datos_banco_mundial()