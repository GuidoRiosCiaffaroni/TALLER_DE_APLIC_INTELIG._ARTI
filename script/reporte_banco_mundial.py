#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script optimizado para entornos Linux.
Extrae indicadores socioeconómicos clave del Banco Mundial para Chile.
"""

import os
import sys
import argparse
import requests
import pandas as pd

def generar_reporte_banco_mundial_chile(rango_anios="1960:2023", pais="CHL"):
    """
    Consulta la API oficial del Banco Mundial, extrae 8 indicadores socioeconómicos
    clave y guarda el resultado en un archivo CSV en el directorio local de Linux.
    """
    nombre_archivo = f"datos_bancomundial_{pais.lower()}_{rango_anios.replace(':', '_')}.csv"

    # Diccionario de mapeo: Códigos de la API oficiales vs Nombres de columnas limpios
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

    df_final = pd.DataFrame()

    print("🌐 Conectando con los servidores de api.worldbank.org...")
    print(f"📥 Procesando serie histórica ({rango_anios}) para {pais}...")

    # Bucle iterativo para consultar cada indicador de forma independiente
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

    # Validación de datos y ordenamiento cronológico ascendente
    if not df_final.empty:
        df_final = df_final.sort_values('Anio').reset_index(drop=True)

        # Guardar localmente usando codificación UTF-8
        df_final.to_csv(nombre_archivo, index=False, encoding='utf-8')

        print("\n" + "="*60)
        print("✅ ¡PROCESO COMPLETADO EXITOSAMENTE!")
        print(f"📁 Archivo guardado en: {os.path.abspath(nombre_archivo)}")
        print(f"📊 Dimensiones finales: {df_final.shape[0]} filas x {df_final.shape[1]} columnas")
        print("="*60)
        
        # Verificación del archivo (Reemplazado display() por print())
        verificar_archivo(nombre_archivo)
    else:
        print("❌ Error crítico: No se pudieron consolidar los datos de la API.", file=sys.stderr)
        sys.exit(1)

def verificar_archivo(ruta_archivo):
    """Lee y muestra las primeras filas del archivo generado en la terminal."""
    try:
        df_verificacion = pd.read_csv(ruta_archivo)
        print(f"\n📋 Primeros 5 registros del archivo verificado:")
        print(df_verificacion.head(5).to_string(index=False))
    except Exception as e:
        print(f"❌ Error al verificar el archivo: {e}", file=sys.stderr)

if __name__ == "__main__":
    # Gestión de argumentos desde la CLI de Linux
    parser = argparse.ArgumentParser(description="Extractor de datos socioeconómicos del Banco Mundial.")
    parser.add_argument("--years", type=str, default="1960:2023", help="Rango de años (Ej: 1960:2023)")
    parser.add_argument("--country", type=str, default="CHL", help="Código ISO del país (Ej: CHL)")
    
    args = parser.parse_args()
    generar_reporte_banco_mundial_chile(rango_anios=args.years, pais=args.country)