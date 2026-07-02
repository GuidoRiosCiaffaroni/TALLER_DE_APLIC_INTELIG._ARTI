from pathlib import Path
import pandas as pd

def procesar_datos_banco_mundial():
    # 1. Obtener la ruta del directorio donde está guardado este script (Tu_Proyecto/script)
    script_dir = Path(__file__).resolve().parent
    
    # 2. Moverse un nivel arriba (raíz) y acceder a la carpeta hermana 'Data'
    data_dir = script_dir.parent / "Data"
    
    # 3. Definir las rutas absolutas calculadas para los archivos
    ruta_entrada = data_dir / "datos_bancomundial_chl_1960_2026.csv"
    ruta_salida = data_dir / "datos_bancomundial_procesados.csv"

    # Verificación de seguridad de la existencia del archivo de entrada
    if not ruta_entrada.exists():
        print(f"[ERROR] No se encontró el archivo original en la ruta esperada:\n --> {ruta_entrada}")
        return

    print(f"[PROCESO] Cargando archivo de datos desde: {ruta_entrada.name}")
    # Lectura del CSV original
    df = pd.read_csv(ruta_entrada)
    print(f"[PROCESO] Registros importados: {len(df)}")

    # TAREA 1: Insertar la columna 'ID' autoincremental al inicio (columna 0)
    df.insert(0, 'ID', range(1, len(df) + 1))
    
    # TAREA 2: Crear la columna 'origen' asignando el valor constante 'WB'
    df['origen'] = 'WB'

    # Asegurar de forma defensiva que el directorio 'Data' exista antes de escribir
    data_dir.mkdir(parents=True, exist_ok=True)

    # Guardar el DataFrame resultante en la carpeta Data
    print(f"[PROCESO] Exportando archivo transformado a: {ruta_salida.name}")
    df.to_csv(ruta_salida, index=False)
    print("[ÉXITO] El archivo procesado ha sido generado correctamente.")

if __name__ == "__main__":
    procesar_datos_banco_mundial()