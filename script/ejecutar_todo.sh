#!/usr/bin/env bash

# ==============================================================================
# SCRIPT ORQUESTADOR: AUTOMATIZACIÓN DE PERMISOS Y EJECUCIÓN EN PIPELINE
# ==============================================================================
# Este script otorga permisos de ejecución de manera masiva y corre
# de forma secuencial los 3 pipelines de extracción de datos socioeconómicos.
# ==============================================================================

# Otorgar permisos totales de lectura, escritura y ejecución
chmod 777 reporte_banco_mundial.py
chmod 777 reporte_cepal_linux.py
chmod 777 reporte_chile_abierto.py

# Lanzar ejecuciones secuenciales
./reporte_banco_mundial.py
./reporte_cepal_linux.py
./reporte_chile_abierto.py