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
    Extrae indicadores socioeconómicos y múltiples variantes del PIB desde la 
    API del Banco Mundial, los consolida en un único DataFrame indexado por año, 
    maneja errores de red y exporta los resultados en un archivo fijo dentro 
    del directorio '../Data' relativo a la ubicación del script.

    Parámetros:
    ----------
    pais : str (default: "CHL")
        Código ISO-Alpha3 del país a consultar (ej. "CHL", "ARG", "BRA").
    rango_anios : str (default: "1960:2026")
        Intervalo temporal estructurado como 'AñoInicio:AñoFin'.
    """
    # 📁 Apunta a la carpeta 'Data' ubicada un nivel arriba de la carpeta 'script'
    directorio_salida = os.path.join("..", "Data")
    
    # Creación segura en caso de que se ejecute desde otra raíz
    if not os.path.exists(directorio_salida):
        os.makedirs(directorio_salida)
        print(f"📁 Directorio verificado/creado: {directorio_salida}/")

    # 📄 Nombre estático del archivo alineado con tu estructura
    nombre_base = "datos_cepal_chl_1960_2026.csv"
    nombre_archivo = os.path.join(directorio_salida, nombre_base)

    # Diccionario de mapeo ampliado para incluir variantes analíticas del PIB
    indicadores = {
        'NY.GDP.MKTP.KD': 'PIB_Precios_Constantes',          # PIB Real (Volumen)
        'NY.GDP.MKTP.CD': 'PIB_Corriente_USD',               # PIB Nominal (Valor absoluto)
        'NY.GDP.MKTP.KD.ZG': 'PIB_Crecimiento_Anual_Porcentaje', # Tasa de crecimiento económico
        'NY.GDP.PCAP.KD': 'Ingreso_Per_Capita_USD',
        'SP.POP.TOTL': 'Poblacion_Total',
        'SM.POP.NETM': 'Migracion_Neta',
        'SI.POV.DDAY': 'Pobreza_Tasa_Armonizada_CEPAL',
        'SL.UEM.TOTL.ZS': 'Desempleo_Porcentaje',
        'FP.CPI.TOTL.ZG': 'Inflacion_Porcentaje',
        'VC.IHR.PSRC.P5': 'Homicidios_Por_100k'
    }

    # Inicialización del DataFrame maestro
    df_final = pd.DataFrame()

    print("============================================================")
    print("🌐 [BLOQUE 1 & 2]: EXTRACCIÓN DESDE ENDPOINTS DE DATOS")
    print("============================================================")
    print(f"📥 Procesando serie histórica CEPAL ({rango_anios}) para {pais}...")

    # Bucle de extracción por indicador
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
                print(f"⚠️ Alerta: Error HTTP {respuesta.status_code} en indicador CEPAL: {nombre_col}", file=sys.stderr)

        except requests.exceptions.RequestException as e:
            print(f"❌ Error de conexión al procesar variable {nombre_col}: {e}", file=sys.stderr)

    # Validación de integridad y persistencia
    if not df_final.empty:
        df_final = df_final.sort_values('Anio').reset_index(drop=True)
        
        # Guarda el archivo en la ruta relativa correcta ../Data/datos_cepal_chl_1960_2026.csv
        df_final.to_csv(nombre_archivo, index=False, encoding='utf-8')
        
        print(f"✅ Archivo CSV guardado exitosamente en: {os.path.abspath(nombre_archivo)}")
        print(f"📊 Dimensiones finales: {df_final.shape[0]} filas x {df_final.shape[1]} columnas")
        
        print("\n============================================================")
        print("📋 [BLOQUE 3]: VISTA PREVIA DE LOS ÚLTIMOS 5 AÑOS REGISTRADOS")
        print("============================================================")
        print(df_final.tail(5).to_string(index=False))
        print("============================================================")
        
    else:
        print("❌ Error crítico: No se pudieron consolidar los datos de las series de la CEPAL.", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extractor de Indicadores Armonizados de la CEPAL.")
    parser.add_argument("--country", type=str, default="CHL", help="Código ISO del país (Ej: CHL)")
    parser.add_argument("--years", type=str, default="1960:2026", help="Rango temporal (Ej: 1960:2026)")
    
    args = parser.parse_args()
    generar_reporte_cepal_chile(pais=args.country, rango_anios=args.years)