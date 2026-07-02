from pathlib import Path
import pandas as pd

def pipeline_preprocesamiento_cepal():
    # 1. Ubicación dinámica basada en el script (Tu_Proyecto/script)
    script_path = Path(__file__).resolve()
    script_dir = script_path.parent
    
    # 2. Apuntar a la carpeta hermana 'Data'
    data_dir = script_dir.parent / "Data"
    
    # 3. Buscar archivos CSV que falten por procesar
    archivos_csv = list(data_dir.glob("*.csv"))
    archivos_entrada = [f for f in archivos_csv if "_preprocesados" not in f.name]

    if not archivos_entrada:
        print(f"[ERROR] No se encontró ningún archivo CSV base en: {data_dir}")
        return

    # IMPORTANTE: Si tienes ambos archivos en la carpeta, aquí procesaremos el primero de la lista.
    # Para asegurar que procese el nuevo de la CEPAL si están juntos, puedes especificar el nombre 
    # o dejar que el bucle procese el archivo detectado. En este caso toma el primero disponible:
    ruta_entrada = archivos_entrada[0]
    
    # Si quieres forzar a que sea estrictamente el de la CEPAL descomenta la siguiente línea:
    # ruta_entrada = data_dir / "datos_cepal_chl_1960_2026.csv"
    
    # Definir el nombre de salida usando el sufijo '_preprocesados'
    ruta_salida = data_dir / f"{ruta_entrada.stem}_preprocesados.csv"

    print(f"[INFO] Script ejecutado: '{script_path.name}'")
    print(f"[INFO] Procesando archivo de datos: '{ruta_entrada.name}'")
    
    # 4. Carga y transformación con Pandas
    df = pd.read_csv(ruta_entrada)
    print(f"[PROCESO] Cantidad de registros encontrados: {len(df)}")

    # TAREA 1: Agregar columna 'ID' correlativa (empezando en 1) al inicio de la tabla (índice 0)
    df.insert(0, 'ID', range(1, len(df) + 1))
    
    # TAREA 2: Agregar columna 'origen' con el valor constante 'WB' (o puedes cambiarlo a 'CEPAL' si lo prefieres)
    df['origen'] = 'WB'

    # 5. Guardar el resultado en la carpeta Data
    print(f"[PROCESO] Exportando resultado a: '{ruta_salida.name}'")
    df.to_csv(ruta_salida, index=False)
    print("[ÉXITO] El preprocesamiento de datos ha concluido correctamente.")

if __name__ == "__main__":
    pipeline_preprocesamiento_cepal()