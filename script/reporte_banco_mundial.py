#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Módulo de Extracción de Datos Socioeconómicos del Banco Mundial.

Este script automatiza la descarga, consolidación y exportación de indicadores
clave de desarrollo para un país y rango de años específicos, utilizando la API
pública REST (v2) del Banco Mundial. El resultado se estructura en un DataFrame
de Pandas y se persiste localmente en formato CSV.

Diseñado para ejecuciones tanto programadas (ETL/Cron) como interactivas en entornos Linux.

Dependencias externas:
    - requests: Para la gestión de peticiones HTTP/REST.
    - pandas: Para la manipulación, alineación y exportación de las series temporales.
"""

import os
import sys
import argparse
import requests
import pandas as pd

def generar_reporte_banco_mundial_chile(rango_anios="1960:2026", pais="CHL"):
    """
    Orquesta la extracción, transformación y carga (ETL) de los indicadores del Banco Mundial.
    
    Itera sobre un diccionario de indicadores predefinidos, realiza peticiones concurrentes
    o secuenciales a la API, limpia las respuestas JSON individuales, alinea los datos 
    cronológicamente mediante un 'outer join' por año y exporta un reporte consolidado en CSV.

    Parámetros:
        rango_anios (str): Período de tiempo consultado en formato 'AAAA:AAAA'. 
                           Por defecto es "1960:2023".
        pais (str): Código alfa-3 (ISO 3166-1) representativo del país objeto de estudio. 
                    Por defecto es "CHL" (Chile).

    Retorno:
        None: La función escribe el resultado directamente en el sistema de archivos local
              y finaliza la ejecución del script con un código de salida (sys.exit) si falla.
    """
    # Definición dinámica del nombre del archivo de salida según los parámetros de la CLI
    nombre_archivo = f"datos_bancomundial_{pais.lower()}_{rango_anios.replace(':', '_')}.csv"

    # Diccionario de mapeo: Claves contienen los códigos oficiales de la API del BM;
    # Valores definen los nombres de columna normalizados (limpios) para el DataFrame final.
    indicadores = {
        'NY.GDP.MKTP.CD': 'PIB_USD',
        'SP.POP.TOTL': 'Poblacion_Total',
        'NY.GDP.PCAP.CD': 'Ingreso_Per_Capita_USD',
        'SM.POP.NETM': 'Migracion_Neta',
        'SI.POV.NAHC': 'Pobreza_Tasa_Nacional_Porcentaje',
        'SL.UEM.TOTL.ZS': 'Desempleo_Porcentaje',
        'FP.CPI.TOTL.ZG': 'Inflacion_Porcentaje',
        'VC.IHR.PSRC.P5': 'Homicidios_Por_100k'
    }

    # Inicialización del DataFrame maestro donde se consolidarán todas las series de datos
    df_final = pd.DataFrame()

    print("🌐 Conectando con los servidores de api.worldbank.org...")
    print(f"📥 Procesando serie histórica ({rango_anios}) para {pais}...")

    # Bucle iterativo para consultar cada indicador de forma independiente (Secuencial)
    for cod_api, nombre_col in indicadores.items():
        # Construcción de la URL RESTful de la API v2. Se fuerza formato JSON y se eleva
        # el parámetro 'per_page' a 1000 para evitar la paginación y traer la serie de un solo viaje.
        url = f"https://api.worldbank.org/v2/country/{pais}/indicator/{cod_api}?format=json&per_page=1000&date={rango_anios}"

        try:
            # Petición HTTP GET con un timeout estricto de 15 segundos para evitar bloqueos indefinidos
            respuesta = requests.get(url, timeout=15)

            # Control de flujo operativo basado en códigos de estado HTTP
            if respuesta.status_code == 200:
                json_data = respuesta.json()

                # La API del BM devuelve una lista donde el índice 0 contiene metadatos de paginación
                # y el índice 1 contiene la lista de registros con los datos económicos reales.
                if len(json_data) > 1 and json_data[1] is not None:
                    registros = json_data[1]

                    # List Comprehension para parsear el JSON y extraer solo el año (Date) y el valor numérico
                    datos_extraidos = [{'Anio': int(r['date']), nombre_col: r['value']} for r in registros]
                    df_temporal = pd.DataFrame(datos_extraidos)

                    # Integración de la serie temporal en el DataFrame maestro
                    if df_final.empty:
                        # Primer indicador procesado inicializa la estructura de la tabla
                        df_final = df_temporal
                    else:
                        # Los siguientes indicadores se fusionan mediante un 'outer join' sobre la columna 'Anio'.
                        # Esto asegura la persistencia de las filas aun cuando existan nulos (NaN) en años específicos.
                        df_final = pd.merge(df_final, df_temporal, on='Anio', how='outer')
            else:
                # Alerta no bloqueante enviada al canal estándar de errores (stderr)
                print(f"⚠️ Alerta: Error HTTP {respuesta.status_code} en el indicador: {nombre_col}", file=sys.stderr)

        except requests.exceptions.RequestException as e:
            # Captura resiliente de fallos de red, DNS o timeouts sin corromper el procesamiento global
            print(f"❌ Error de conexión al procesar {nombre_col}: {e}", file=sys.stderr)

    # Fase de Validación, Ordenamiento y Persistencia (Carga)
    if not df_final.empty:
        # Ordenamiento explícito cronológico ascendente (de pasado a presente)
        df_final = df_final.sort_values('Anio').reset_index(drop=True)

        # Volcado de datos a disco en formato CSV delimitado por comas, preservando caracteres especiales
        df_final.to_csv(nombre_archivo, index=False, encoding='utf-8')

        print("\n" + "="*60)
        print("✅ ¡PROCESO COMPLETADO EXITOSAMENTE!")
        print(f"📁 Archivo guardado en: {os.path.abspath(nombre_archivo)}")
        print(f"📊 Dimensiones finales: {df_final.shape[0]} filas x {df_final.shape[1]} columnas")
        print("="*60)
        
        # Auditoría inmediata post-escritura
        verificar_archivo(nombre_archivo)
    else:
        # Interrupción drástica de la ejecución si no se logró estructurar ninguna información
        print("❌ Error crítico: No se pudieron consolidar los datos de la API.", file=sys.stderr)
        sys.exit(1)

def verificar_archivo(ruta_archivo):
    """
    Realiza un sanity check (control de calidad rápido) leyendo el CSV generado de vuelta a memoria.

    Muestra una vista previa de las primeras 5 observaciones directamente en la terminal estándar.

    Parámetros:
        ruta_archivo (str): Ruta relativa o absoluta del archivo CSV a auditar.
    """
    try:
        # Lectura de verificación para confirmar que el archivo no está corrupto
        df_verificacion = pd.read_csv(ruta_archivo)
        print(f"\n📋 Primeros 5 registros del archivo verificado:")
        # to_string(index=False) suprime la columna de índices autogenerados, limpiando la salida CLI
        print(df_verificacion.head(5).to_string(index=False))
    except Exception as e:
        print(f"❌ Error al verificar el archivo: {e}", file=sys.stderr)

if __name__ == "__main__":
    # Configuración e inicialización del analizador de argumentos de línea de comandos (CLI)
    parser = argparse.ArgumentParser(
        description="Extractor automatizado de datos socioeconómicos del Banco Mundial optimizado para analistas."
    )
    
    # Argumento posicional/opcional para el rango de tiempo
    parser.add_argument(
        "--years", 
        type=str, 
        default="1960:2026", 
        help="Rango cronológico de consulta estructurado como 'Inicio:Fin' (Ejemplo: 1960:2026)"
    )
    
    # Argumento posicional/opcional para el código del país objetivo
    parser.add_argument(
        "--country", 
        type=str, 
        default="CHL", 
        help="Código de país bajo la norma ISO 3166-1 alfa-3 de 3 caracteres (Ejemplo: CHL, ARG, BRA)"
    )
    
    # Mapeo y parsing de los argumentos inyectados por la terminal
    args = parser.parse_args()
    
    # Ejecución principal del script usando los parámetros validados de la CLI
    generar_reporte_banco_mundial_chile(rango_anios=args.years, pais=args.country)