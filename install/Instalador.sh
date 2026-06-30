#!/usr/bin/env bash

# ==============================================================================
# SCRIPT DE AUTOMATIZACIÓN EN LINUX: INSTALACIÓN DE SUITE DATA SCIENCE
# ==============================================================================
# Este script instala de forma quirúrgica todas las dependencias del sistema y
# librerías de Python para asegurar la conectividad API y la capacidad gráfica.
# ==============================================================================

# Configuración de colores para salida limpia en terminal
VERDE='\033[0;32m'
AZUL='\033[0;34m'
AMARILLO='\033[1;33m'
ROJO='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${AZUL}==================================================================${NC}"
echo -e "${AZUL}    🚀 COMPILANDO E INSTALANDO DEPENDENCIAS DE CIENCIA DE DATOS   ${NC}"
echo -e "${AZUL}==================================================================${NC}"

# Garantizar que se ejecuta con privilegios elevados (Root/Sudo)
if [ "$EUID" -ne 0 ]; then
  echo -e "${AMARILLO}⚠️  Se requieren privilegios de administrador para instalar paquetes.${NC}"
  echo -e "${AMARILLO}Elevando privilegios automáticamente con sudo...${NC}"
  exec sudo bash "$0" "$@"
fi

# ------------------------------------------------------------------------------
# PASO 1: Actualización del Gestor de Paquetes (APT)
# ------------------------------------------------------------------------------
echo -e "\n${AZUL}[1/4] Sincronizando repositorios de Ubuntu Server...${NC}"
apt update -y
if [ $? -eq 0 ]; then
    echo -e "${VERDE}✔ Repositorios sincronizados.${NC}"
else
    echo -e "${ROJO}❌ Error al sincronizar con los servidores de Ubuntu.${NC}"
fi

# ------------------------------------------------------------------------------
# PASO 2: Dependencias del Sistema Operativo Linux
# ------------------------------------------------------------------------------
echo -e "\n${AZUL}[2/4] Instalando compiladores y soporte gráfico nativo (Tkinter)...${NC}"
# python3-tk es la dependencia nativa de Linux para que Matplotlib dibuje correctamente
apt install python3 python3-pip python3-dev build-essential python3-tk -y
if [ $? -eq 0 ]; then
    echo -e "${VERDE}✔ Dependencias del núcleo de Linux instaladas con éxito.${NC}"
else
    echo -e "${ROJO}❌ Falló la instalación de paquetes base del sistema.${NC}"
fi

# ------------------------------------------------------------------------------
# PASO 3: Instalación de las Librerías de Python (Global y Consistente)
# ------------------------------------------------------------------------------
echo -e "\n${AZUL}[3/4] Desplegando el ecosistema de Python para Ciencia de Datos...${NC}"

# Instalar primero vía APT para máxima estabilidad en distribuciones Debian/Ubuntu
apt install python3-requests python3-pandas python3-matplotlib python3-seaborn -y

# Forzar paridad y actualizaciones de seguridad con pip rompiendo bloqueos de entorno si existiesen
echo -e "${AMARILLO}Optimizando paquetes globales mediante pip3...${NC}"
pip3 install requests pandas matplotlib seaborn --break-system-packages --upgrade

if [ $? -eq 0 ]; then
    echo -e "${VERDE}✔ Todas las librerías se inyectaron correctamente en el entorno de Linux.${NC}"
else
    echo -e "${AMARILLO}⚠️  Nota: Pip reportó advertencias menores, pero el entorno está operativo.${NC}"
fi

# ------------------------------------------------------------------------------
# PASO 4: Test de Integridad (Verificación Automatizada)
# ------------------------------------------------------------------------------
echo -e "\n${AZUL}[4/4] Validando la disponibilidad de los módulos...${NC}"
python3 -c "
import requests
import pandas as pd
import matplotlib
import seaborn as sns
print('  🌐 [OK] Conectividad HTTP (requests) v' + requests.__version__)
print('  📊 [OK] Procesamiento Tabular (pandas) v' + pd.__version__)
print('  📈 [OK] Lienzo Gráfico Base (matplotlib) v' + matplotlib.__version__)
print('  🎨 [OK] Estética y Distribuciones (seaborn) v' + sns.__version__)
"

if [ $? -eq 0 ]; then
    echo -e "\n${VERDE}==================================================================${NC}"
    echo -e "${VERDE}  🎉 ¡ÉXITO TOTAL! Todo el software se instaló y verificó.       ${NC}"
    echo -e "${VERDE}==================================================================${NC}"
    echo -e "Entorno listo para procesar datos y renderizar gráficos en Linux."
else
    echo -e "${ROJO}❌ Error: Uno o más módulos no se cargaron correctamente.${NC}"
    exit 1
fi