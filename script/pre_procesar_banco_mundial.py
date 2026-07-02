from pathlib import Path
import pandas as pd

def pipeline_totalmente_dinamico():
    # 1. Obtener la ubicación de este script de forma dinámica
    # No importa el nombre del .py, __file__ siempre captura su ruta actual
    script_path = Path(__file__).resolve()
    script_dir = script_path.parent
    
    # 2. Apuntar a la carpeta hermana 'Data'
    data_dir = script_dir.parent / "Data"
    
    # 3. Buscar el archivo CSV original en 'Data/' (omitiendo los ya procesados)
    archivos_csv = list(data_dir.glob("*.csv"))
    archivos_entrada = [f for f in archivos_csv if "_procesados" not in f.name]

    if not archivos_entrada:
        print(f"[ERROR] No se encontró ningún archivo CSV base en: {data_dir}")
        return

    # Tomar el archivo CSV disponible en la carpeta
    ruta_entrada = archivos_entrada[0]
    
    # Definir el nombre de salida basado en el nombre real del CSV encontrado
    ruta_salida = data_dir / f"{ruta_entrada.stem}_procesados.csv"

    print(f"[INFO] Script ejecutado: '{script_path.name}'")
    print(f"[INFO] Procesando archivo de datos: '{ruta_entrada.name}'")
    
    # 4. Carga y transformación con Pandas
    df = pd.read_csv(ruta_entrada)
    print(f"[PROCESO] Cantidad de registros: {len(df)}")

    # TAREA 1: Agregar columna 'ID' correlativa (empezando en 1) al inicio
    df.insert(0, 'ID', range(1, len(df) + 1))
    
    # TAREA 2: Agregar columna 'origen' con el valor constante 'WB'
    df['origen'] = 'WB'

    # 5. Guardar el resultado en la carpeta Data
    print(f"[PROCESO] Exportando resultado a: '{ruta_salida.name}'")
    df.to_csv(ruta_salida, index=False)
    print("[ÉXITO] El proceso ha concluido correctamente.")

if __name__ == "__main__":
    pipeline_totalmente_dinamico()