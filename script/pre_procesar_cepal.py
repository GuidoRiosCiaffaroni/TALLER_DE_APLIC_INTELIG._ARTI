from pathlib import Path
import pandas as pd

def pipeline_preprocesamiento_cepal_fijo():
    # 1. Ubicación dinámica basada en el script (Tu_Proyecto/script)
    script_path = Path(__file__).resolve()
    script_dir = script_path.parent
    
    # 2. Apuntar a la carpeta hermana 'Data' subiendo un nivel
    data_dir = script_dir.parent / "Data"
    
    # 3. Forzar la ruta exacta del archivo origen de la CEPAL
    ruta_entrada = data_dir / "datos_cepal_chl_1960_2026.csv"
    
    # Definir el nombre exacto de salida
    ruta_salida = data_dir / "datos_cepal_chl_1960_2026_preprocesados.csv"

    print(f"[INFO] Script ejecutado de forma estricta: '{script_path.name}'")

    # 4. Control de excepciones manual por si el archivo no está en Data/
    if not ruta_entrada.exists():
        print(f"[ERROR] No se encontró el archivo base en la ruta esperada:")
        print(f" --> {ruta_entrada}")
        print("\nVerifica lo siguiente:")
        print(f" 1. Que estés ejecutando el script desde la carpeta del proyecto.")
        print(f" 2. Que el archivo se llame exactamente 'datos_cepal_chl_1960_2026.csv' dentro de 'Data'.")
        return

    print(f"[PROCESO] Leyendo: '{ruta_entrada.name}'")
    
    # 5. Carga y transformación con Pandas
    df = pd.read_csv(ruta_entrada)
    print(f"[PROCESO] Cantidad de registros encontrados: {len(df)}")

    # TAREA 1: Agregar columna 'ID' correlativa (empezando en 1) al inicio de la tabla
    df.insert(0, 'ID', range(1, len(df) + 1))
    
    # TAREA 2: Agregar columna 'origen' con la descripción "CP"
    df['origen'] = 'CP'

    # Asegurar que el directorio de salida exista
    data_dir.mkdir(parents=True, exist_ok=True)

    # 6. Guardar el resultado en la carpeta Data
    print(f"[PROCESO] Exportando resultado a: '{ruta_salida.name}'")
    df.to_csv(ruta_salida, index=False)
    print("[ÉXITO] El archivo preprocesado ha sido generado y guardado en la carpeta Data.")

if __name__ == "__main__":
    pipeline_preprocesamiento_cepal_fijo()