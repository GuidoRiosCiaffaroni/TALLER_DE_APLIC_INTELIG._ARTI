from pathlib import Path
import pandas as pd

def procesar_datos_especificos():
    # 1. Configurar las rutas relativas basadas en la ubicación del script
    # __file__ apunta a: tu_proyecto/script/nombre_del_script.py
    script_dir = Path(__file__).resolve().parent
    
    # Referencia a la carpeta hermana 'Data' (sube un nivel y entra a Data)
    data_dir = script_dir.parent / "Data"
    
    # Rutas exactas para tu archivo específico
    ruta_entrada = data_dir / "datos_bancomundial_chl_1960_2026.csv"
    ruta_salida = data_dir / "datos_bancomundial_procesados.csv"

    # 2. Control de existencia del archivo en la carpeta 'Data'
    if not ruta_entrada.exists():
        print(f"Error: No se encontró el archivo específico en: {ruta_entrada}")
        print("Asegúrate de haber guardado 'datos_bancomundial_chl_1960_2026.csv' dentro de la carpeta 'Data'.")
        return

    print(f"Leyendo archivo de datos desde: {ruta_entrada}")
    df = pd.read_csv(ruta_entrada)
    print(f"Cantidad de registros a procesar: {len(df)}")

    # TAREA 1: Agregar columna 'ID' numerada consecutivamente desde 1 al principio de la tabla
    df.insert(0, 'ID', range(1, len(df) + 1))
    
    # TAREA 2: Agregar columna 'origen' con la constante 'WB' para todas las filas
    df['origen'] = 'WB'

    # 3. Garantizar que la carpeta de destino exista antes de escribir el archivo
    data_dir.mkdir(parents=True, exist_ok=True)

    # 4. Exportar el DataFrame resultante a la carpeta 'Data'
    print(f"Exportando archivo procesado a: {ruta_salida}")
    df.to_csv(ruta_salida, index=False)
    print("¡Proceso de datos finalizado con éxito!")

if __name__ == "__main__":
    procesar_datos_especificos()