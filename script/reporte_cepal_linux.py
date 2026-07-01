#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
==============================================================================
SISTEMA DE EXTRACCIÓN Y DOCUMENTACIÓN DE INDICADORES ARMONIZADOS CEPAL / ONU
==============================================================================
UTILIDAD DE LAS LIBRERÍAS INCORPORADAS:
1. 'requests': Establece la comunicación HTTP con los endpoints de datos.
2. 'pandas':   Fusiona las series históricas mediante un outer-merge cronológico.
==============================================================================
"""

import os
import sys
import argparse
import requests
import pandas as pd

def generar_reporte_cepal_chile(pais="CHL", rango_anios="1960:2026"):
    """
    Extrae 8 indicadores socioeconómicos clave desde la API del Banco Mundial,
    los consolida en un único DataFrame indexado por año, maneja errores de red
    y exporta los resultados de forma estructurada en un archivo fijo llamado
    'datos_cepal_chl_1960_2026.csv' dentro del directorio 'Data'.

    Parámetros:
    ----------
    pais : str (default: "CHL")
        Código ISO-Alpha3 del país a consultar (ej. "CHL", "ARG", "BRA").
    rango_anios : str (default: "1960:2026")
        Intervalo temporal estructurado como 'AñoInicio:AñoFin'.
    """
    # 📁 Configuración y creación segura del directorio 'Data'
    directorio_salida = "Data"
    if not os.path.exists(directorio_salida):
        os.makedirs(directorio_salida)
        print(f"📁 Directorio creado: {directorio_salida}/")

    # 📄 Nombre estático del archivo solicitado por el usuario
    nombre_base = "datos_cepal_chl_1960_2026.csv"
    nombre_archivo = os.path.join(directorio_salida, nombre_base)

    # Diccionario de mapeo: Vincula el código técnico de la API (Key) con un nombre legible en español (Value)
    indicadores = {
        'NY.GDP.MKTP.KD': 'PIB_Precios_Constantes',
        'SP.POP.TOTL': 'Poblacion_Total',
        'NY.GDP.PCAP.KD': 'Ingreso_Per_Capita_USD',
        'SM.POP.NETM': 'Migracion_Neta',
        'SI.POV.DDAY': 'Pobreza_Tasa_Armonizada_CEPAL',
        'SL.UEM.TOTL.ZS': 'Desempleo_Porcentaje',
        'FP.CPI.TOTL.ZG': 'Inflacion_Porcentaje',
        'VC.IHR.PSRC.P5': 'Homicidios_Por_100k'
    }

    # Inicialización del DataFrame maestro donde se acumularán y acoplarán todas las series
    df_final = pd.DataFrame()

    print("============================================================")
    print("🌐 [BLOQUE 1 & 2]: EXTRACCIÓN DESDE ENDPOINTS DE DATOS")
    print("============================================================")
    print(f"📥 Procesando serie histórica CEPAL ({rango_anios}) para {pais}...")

    # Bucle de extracción por indicador
    for cod_api, nombre_col in indicadores.items():
        # URL REST para la API v2 del Banco Mundial
        url = f"https://api.worldbank.org/v2/country/{pais}/indicator/{cod_api}?format=json&per_page=1000&date={rango_anios}"

        try:
            # Petición HTTP GET con un timeout de 15 segundos para evitar bloqueos
            respuesta = requests.get(url, timeout=15)

            if respuesta.status_code == 200:
                json_data = respuesta.json()

                # Estructura de la API: [0] contiene paginación, [1] contiene el array de datos
                if len(json_data) > 1 and json_data[1] is not None:
                    registros = json_data[1]
                    
                    # Extracción del año y valor de cada registro
                    datos_extraidos = [{'Anio': int(r['date']), nombre_col: r['value']} for r in registros]
                    df_temporal = pd.DataFrame(datos_extraidos)

                    # Consolidación de datos estructurales (Pandas Integration)
                    if df_final.empty:
                        df_final = df_temporal
                    else:
                        # Outer Merge por Año para no perder información si hay nulos
                        df_final = pd.merge(df_final, df_temporal, on='Anio', how='outer')
            else:
                print(f"⚠️ Alerta: Error HTTP {respuesta.status_code} en indicador CEPAL: {nombre_col}", file=sys.stderr)

        except requests.exceptions.RequestException as e:
            print(f"❌ Error de conexión al procesar variable {nombre_col}: {e}", file=sys.stderr)

    # Validación de integridad del proceso
    if not df_final.empty:
        # Ordenación cronológica exacta y reseteo del índice
        df_final = df_final.sort_values('Anio').reset_index(drop=True)
        
        # Persistencia en disco (Archivo CSV con el nombre específico)
        df_final.to_csv(nombre_archivo, index=False, encoding='utf-8')
        
        print(f"✅ Archivo CSV guardado exitosamente en: {nombre_archivo}")
        print(f"📊 Dimensiones finales: {df_final.shape[0]} filas x {df_final.shape[1]} columnas")
        
        # --- [BLOQUE 3]: Vista previa en texto plano por terminal ---
        print("\n============================================================")
        print("📋 [BLOQUE 3]: VISTA PREVIA DE LOS ÚLTIMOS 5 AÑOS REGISTRADOS")
        print("============================================================")
        print(df_final.tail(5).to_string(index=False))
        print("============================================================")
        
    else:
        print("❌ Error crítico: No se pudieron consolidar los datos de las series de la CEPAL.", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    # Inicialización del analizador de argumentos de línea de comandos
    parser = argparse.ArgumentParser(description="Extractor de Indicadores Armonizados de la CEPAL.")
    parser.add_argument("--country", type=str, default="CHL", help="Código ISO del país (Ej: CHL)")
    parser.add_argument("--years", type=str, default="1960:2026", help="Rango temporal (Ej: 1960:2026)")
    
    args = parser.parse_args()
    
    # Orquestación principal
    generar_reporte_cepal_chile(pais=args.country, rango_anios=args.years)