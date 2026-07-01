#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Módulo de Extracción de Datos Socioeconómicos del Banco Mundial.

Este script automatiza la descarga, consolidación y exportación de indicadores
clave de desarrollo para un país y rango de años específicos, utilizando la API
pública REST (v2) del Banco Mundial. El resultado se estructura en un DataFrame
de Pandas y se persiste localmente en formato CSV dentro del directorio 'Data/' 
situado en la raíz del proyecto.

Diseñado para ejecuciones tanto programadas (ETL/Cron) como interactivas en entornos Linux.

Dependencias externas:
    - requests: Para la gestión de peticiones HTTP/REST.
    - pandas: Para la manipulación, alineación y exportación de las series temporales.
"""

import os
import sys
import argparse
from pathlib import Path
import requests
import pandas as pd

def generar_reporte_banco_mundial_chile(rango_anios="1960:2026", pais="CHL"):
    """
    Orquesta la extracción, transformación y carga (ETL) de los indicadores del Banco Mundial.
    
    Itera sobre un diccionario de indicadores predefinidos, realiza peticiones 
    a la API, limpia las respuestas JSON individuales, alinea los datos 
    cronológicamente mediante un 'outer join' por año y exporta un reporte 
    consolidado en CSV dentro de la carpeta 'Data/' en la raíz del proyecto.

    Parámetros:
        rango_anios (str): Período de tiempo consultado en formato 'AAAA:AAAA'. 
                           Por defecto es "1960:2026".
        pais (str): Código alfa-3 (ISO 3166-1) representativo del país objeto de estudio. 
                    Por defecto es "CHL" (Chile).
    """
    # 1. Obtener la ruta del script (TALLER_DE_APLIC_INTELIG._ARTI/script)
    ruta_script = os.path.dirname(os.path.abspath(__file__))
    
    # 2. Subir un nivel (a la raíz del proyecto) y apuntar a la carpeta 'Data'
    directorio_data = Path(ruta_script).parent / "Data"
    
    # Crear el directorio 'Data' en la raíz si por alguna razón no existiera
    directorio_data.mkdir(parents=True, exist_ok=True)

    # Definición del nombre y ruta absoluta del archivo de salida
    nombre_archivo = f"datos_bancomundial_{pais.lower()}_{rango_anios.replace(':', '_')}.csv"
    ruta_salida_csv = directorio_data / nombre_archivo

    # Diccionario de mapeo de indicadores
    indicadores = {
        'NY.GDP.MKTP.CD': 'PIB_USD',
        'NY.GDP.PCAP.CD': 'Ingreso_Per_Capita_USD',
        'SP.POP.TOTL': 'Poblacion_Total',
        'SM.POP.NETM': 'Migracion_Neta',
        'SI.POV.NAHC': 'Pobreza_Tasa_Nacional_Porcentaje',
        'SL.UEM.TOTL.ZS': 'Desempleo_Porcentaje',
        'FP.CPI.TOTL.ZG': 'Inflacion_Porcentaje',
        'VC.IHR.PSRC.P5': 'Homicidios_Por_100k'
    }

    df_final = pd.DataFrame()

    print("🌐 Conectando con los servidores de api.worldbank.org...")
    print(f"📥 Procesando serie histórica ({rango_anios}) para {pais}...")

    # Bucle iterativo para consultar cada indicador
    for cod_api, nombre_col in indicadores.items():
        url = f"https://api.worldbank.org/v2/country/{pais}/indicator/{cod_api}?format=json&per_page=1000&date={rango_anios}"

        try:
            respuesta = requests.get(url, timeout=15)

            if respuesta.status_code == 200:
                json_data = respuesta.json()

                if len(json_data) > 1 and json_data[1] is not None:
                    registros = json_data[1]

                    datos_extraidos = [{'Anio': int(r['date']), nombre_col: r['value']} for r in registros]
                    df_temporal = pd.DataFrame(datos_extraidos)

                    if df_final.empty:
                        df_final = df_temporal
                    else:
                        df_final = pd.merge(df_final, df_temporal, on='Anio', how='outer')
            else:
                print(f"⚠️ Alerta: Error HTTP {respuesta.status_code} en el indicador: {nombre_col}", file=sys.stderr)

        except requests.exceptions.RequestException as e:
            print(f"❌ Error de conexión al procesar {nombre_col}: {e}", file=sys.stderr)

    # Fase de Validación, Ordenamiento y Persistencia (Carga)
    if not df_final.empty:
        # Ordenamiento cronológico ascendente
        df_final = df_final.sort_values('Anio').reset_index(drop=True)

        # Volcado de datos directamente a la ruta destino (dentro de la raíz / Data)
        df_final.to_csv(ruta_salida_csv, index=False, encoding='utf-8')

        print("\n" + "="*60)
        print("✅ ¡PROCESO COMPLETADO EXITOSAMENTE!")
        print(f"📁 Archivo guardado en: {ruta_salida_csv}")
        print(f"📊 Dimensiones finales: {df_final.shape[0]} filas x {df_final.shape[1]} columnas")
        print("="*60)
        
        # Auditoría post-escritura pasando la ruta correcta
        verificar_archivo(ruta_salida_csv)
    else:
        print("❌ Error crítico: No se pudieron consolidar los datos de la API.", file=sys.stderr)
        sys.exit(1)

def verificar_archivo(ruta_archivo):
    """
    Realiza un control de calidad rápido leyendo el CSV generado desde su ruta específica.
    """
    try:
        df_verificacion = pd.read_csv(ruta_archivo)
        print(f"\n📋 Primeros 5 registros del archivo verificado:")
        print(df_verificacion.head(5).to_string(index=False))
    except Exception as e:
        print(f"❌ Error al verificar el archivo: {e}", file=sys.stderr)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Extractor automatizado de datos socioeconómicos del Banco Mundial optimizado para analistas."
    )
    
    parser.add_argument(
        "--years", 
        type=str, 
        default="1960:2026", 
        help="Rango cronológico de consulta (Ejemplo: 1960:2026)"
    )
    
    parser.add_argument(
        "--country", 
        type=str, 
        default="CHL", 
        help="Código de país ISO 3166-1 alfa-3 (Ejemplo: CHL, ARG, BRA)"
    )
    
    args = parser.parse_args()
    generar_reporte_banco_mundial_chile(rango_anios=args.years, pais=args.country)