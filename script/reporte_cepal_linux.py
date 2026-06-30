#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
==============================================================================
SISTEMA DE EXTRACCIÓN Y DOCUMENTACIÓN DE INDICADORES ARMONIZADOS CEPAL / ONU
==============================================================================
UTILIDAD DE LAS LIBRERÍAS INCORPORADAS:
1. 'requests': Establece la comunicación HTTP con los endpoints de datos.
2. 'pandas':   Fusiiona las series históricas mediante un outer-merge cronológico.
3. 'matplotlib' & 'seaborn': Diseñan y renderizan las tendencias sin entorno X11.
==============================================================================
"""

# Configuración del backend gráfico para terminales puras de Linux (VirtualBox)
import matplotlib
matplotlib.use('Agg')

import os
import sys
import argparse
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def generar_reporte_cepal_chile(pais="CHL", rango_anios="1960:2023"):
    """
    Extrae los 8 indicadores socioeconómicos clave validados por la CEPAL/ONU,
    los consolida en un DataFrame ordenado y exporta reportes en CSV e imágenes.
    """
    nombre_archivo = f"datos_cepal_{pais.lower()}_{rango_anios.replace(':', '_')}.csv"
    grafico_salida = f"tendencias_cepal_{pais.lower()}.png"

    # Mapeo de Indicadores de las series oficiales regionales CEPAL/ONU:
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

    df_final = pd.DataFrame()

    print("============================================================")
    print("🌐 [BLOQUE 1 & 2]: EXTRACCIÓN DESDE ENDPOINTS DE DATOS")
    print("============================================================")
    print(f"📥 Procesando serie histórica CEPAL ({rango_anios}) para {pais}...")

    # Bucle iterativo de extracción (requests)
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

                    # Consolidación de datos estructurales (pandas)
                    if df_final.empty:
                        df_final = df_temporal
                    else:
                        df_final = pd.merge(df_final, df_temporal, on='Anio', how='outer')
            else:
                print(f"⚠️ Alerta: Error HTTP {respuesta.status_code} en indicador CEPAL: {nombre_col}", file=sys.stderr)

        except requests.exceptions.RequestException as e:
            print(f"❌ Error de conexión al procesar variable {nombre_col}: {e}", file=sys.stderr)

    # Verificación de la integridad de la estructura de datos
    if not df_final.empty:
        df_final = df_final.sort_values('Anio').reset_index(drop=True)
        df_final.to_csv(nombre_archivo, index=False, encoding='utf-8')
        
        print(f"✅ Archivo CSV guardado exitosamente: {nombre_archivo}")
        print(f"📊 Dimensiones finales: {df_final.shape[0]} filas x {df_final.shape[1]} columnas")
        
        # --- [BLOQUE 3]: Inspección por Terminal (Sustituto de display) ---
        print("\n============================================================")
        print("📋 [BLOQUE 3]: VISTA PREVIA DE LOS ÚLTIMOS 5 AÑOS REGISTRADOS")
        print("============================================================")
        print(df_final.tail(5).to_string(index=False))

        # --- [BLOQUE 4]: Renderizado de Gráficos Estadísticos ---
        generar_grafico_reporte(df_final, pais, rango_anios, grafico_salida)
        
    else:
        print("❌ Error crítico: No se pudieron consolidar los datos de las series de la CEPAL.", file=sys.stderr)
        sys.exit(1)

def generar_grafico_reporte(df, pais, rango, output_img):
    """Genera una visualización del comportamiento socioeconómico regional."""
    print("\n============================================================")
    print("🎨 [BLOQUE 4]: GENERACIÓN DE REPORTES GRÁFICOS (CEPAL)")
    print("============================================================")
    print("📈 Trazando curvas de evolución con Matplotlib y Seaborn...")
    
    try:
        sns.set_theme(style="whitegrid")
        fig, axes = plt.subplots(2, 1, figsize=(12, 10), sharex=True)

        # Gráfica Superior: PIB a Precios Constantes
        sns.lineplot(data=df, x="Anio", y="PIB_Precios_Constantes", ax=axes[0], 
                     color="#2ca02c", linewidth=2.5, marker="s", label="PIB (Precios Constantes)")
        axes[0].set_title(f"Evolución del PIB a Precios Constantes - Región {pais}", fontsize=14, fontweight='bold')
        axes[0].set_ylabel("Valor en Escala Monetaria")

        # Gráfica Inferior: Desempleo Armonizado
        sns.lineplot(data=df, x="Anio", y="Desempleo_Porcentaje", ax=axes[1], 
                     color="#ff7f0e", linewidth=2, marker="v", label="Tasa de Desempleo %")
        axes[1].set_title("Tasa Oficial de Desempleo Armonizada", fontsize=12, fontweight='bold')
        axes[1].set_xlabel("Año")
        axes[1].set_ylabel("Porcentaje (%)")

        plt.tight_layout()
        plt.savefig(output_img, dpi=300)
        plt.close()
        
        print(f"✅ Gráfico exportado de forma nativa a: {os.path.abspath(output_img)}")
        print("============================================================")
        
    except Exception as e:
        print(f"❌ Error al procesar renderizado gráfico: {e}", file=sys.stderr)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extractor de Indicadores Armonizados de la CEPAL.")
    parser.add_argument("--country", type=str, default="CHL", help="Código ISO del país (Ej: CHL)")
    parser.add_argument("--years", type=str, default="1960:2023", help="Rango temporal (Ej: 1960:2023)")
    
    args = parser.parse_args()
    generar_reporte_cepal_chile(pais=args.country, rango_anios=args.years)