#!/usr/bin/env bash

# ==============================================================================
# SCRIPT ORQUESTADOR: AUTOMATIZACION DE PERMISOS Y EJECUCION EN PIPELINE
# ==============================================================================
# Este script otorga permisos de ejecucion de manera masiva y corre
# de forma secuencial los 3 pipelines de extraccion de datos socioeconomicos.
# ==============================================================================

# Otorgar permisos de ejecucion de forma segura
chmod +x reporte_banco_mundial.py
chmod +x reporte_cepal_linux.py
chmod +x reporte_chile_abierto.py

# Lanzar ejecuciones secuenciales
./reporte_banco_mundial.py
./reporte_cepal_linux.py
./reporte_chile_abierto.py