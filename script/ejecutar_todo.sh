#!/usr/bin/env bash

# ==============================================================================
# SCRIPT ORQUESTADOR: AUTOMATIZACIÓN DE PERMISOS Y EJECUCIÓN EN PIPELINE
# ==============================================================================
# Este script otorga permisos de ejecución (chmod +x) de manera masiva y corre
# de forma secuencial los 3 pipelines de extracción de datos socioeconómicos.
# ==============================================================================

# Configuración de colores para salida limpia y legible en terminal
VERDE='\033[0;32m'
AZUL='\033[0;34m'
AMARILLO='\033[1;33m'
ROJO='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${AZUL}==================================================================${NC}"
echo -e "${AZUL} ⚡  INICIANDO PANEL CENTRAL DE AUTOMATIZACIÓN (PIPELINE INTEGRAL) ${NC}"
echo -e "${AZUL}==================================================================${NC}"

# Lista de scripts que componen el ecosistema de análisis
SCRIPTS=(
    "reporte_completo_banco_mundial.py"
    "reporte_cepal_linux.py"
    "reporte_chile_abierto.py"
)

# ------------------------------------------------------------------------------
# PASO 1: Gestión Masiva de Permisos en Linux (chmod +x)
# ------------------------------------------------------------------------------
echo -e "\n${AZUL}[1/2] Verificando archivos y aplicando permisos de ejecución...${NC}"

for script in "${SCRIPTS[@]}"; do
    if [ -f "$script" ]; then
        chmod +x "$script"
        echo -e "${VERDE} ✔ Permisos otorgados correctamente a:${NC} $script"
    else
        echo -e "${ROJO} ❌ Error crítico: No se encontró el archivo '$script' en este directorio.${NC}"
        echo -e "${AMARILLO}Asegúrate de que el nombre coincide y estás en la ruta correcta.${NC}"
        exit 1
    fi
done

# ------------------------------------------------------------------------------
# PASO 2: Ejecución Secuencial del Pipeline Completo
# ------------------------------------------------------------------------------
echo -e "\n${AZUL}[2/2] Lanzando la ejecución secuencial de los scripts...${NC}"
echo -e "${AZUL}==================================================================${NC}"

# 1. Ejecutar Script Banco Mundial
echo -e "\n🚀 ${AMARILLO}Ejecutando [1/3]: Banco Mundial...${NC}"
./reporte_completo_banco_mundial.py
if [ $? -eq 0 ]; then
    echo -e "${VERDE}✔ Extracción e informe de Banco Mundial completados.${NC}"
else
    echo -e "${ROJO}❌ Falló el script de Banco Mundial.${NC}"
fi

# 2. Ejecutar Script CEPAL
echo -e "\n🚀 ${AMARILLO}Ejecutando [2/3]: CEPAL Regional...${NC}"
./reporte_cepal_linux.py
if [ $? -eq 0 ]; then
    echo -e "${VERDE}✔ Extracción e informe de CEPAL completados.${NC}"
else
    echo -e "${ROJO}❌ Falló el script de CEPAL.${NC}"
fi

# 3. Ejecutar Script Chile Abierto
echo -e "\n🚀 ${AMARILLO}Ejecutando [3/3]: Mapeo Chile Abierto...${NC}"
./reporte_chile_abierto.py
if [ $? -eq 0 ]; then
    echo -e "${VERDE}✔ Extracción e informe de Chile Abierto completados.${NC}"
else
    echo -e "${ROJO}❌ Falló el script de Chile Abierto.${NC}"
fi

# ------------------------------------------------------------------------------
# Reporte de Cierre e Inspección de Productos Generados
# ------------------------------------------------------------------------------
echo -e "\n${AZUL}==================================================================${NC}"
echo -e "${VERDE} 🎉 ¡PIPELINE INTEGRAL FINALIZADO CON ÉXITO!                      ${NC}"
echo -e "${AZUL}==================================================================${NC}"
echo -e "\n📊 ${AMARILLO}Archivos CSV y Gráficos disponibles en el directorio:${NC}"

# Comando nativo de Linux para listar los entregables generados
ls -lh datos_*.csv evolucion_*.png tendencias_*.png distribucion_*.png 2>/dev/null

echo -e "${AZUL}==================================================================${NC}"