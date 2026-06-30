#!/usr/bin/env bash

# ==============================================================================
# SCRIPT DE CONFIGURACIÓN DE ENTORNO LINUX
# ==============================================================================
# - e: Detiene el script si algún comando falla.
# - u: Falla si se intenta usar una variable no declarada.
# - o pipefail: Captura errores en tuberías (pipelines).
set -euo pipefail

echo -e "\e[1;34m=== [1/4] Actualizando repositorios e instalando dependencias del sistema ] ===\e[0m"
# Actualizamos el gestor de paquetes APT e instalamos el soporte para entornos virtuales de Python 3
sudo apt-get update -y
sudo apt-get install -y python3-pip python3-venv python3-dev

echo -e "\n\e[1;34m=== [2/4] Creando el entorno virtual de Python (VENV) ] ===\e[0m"
# Creamos una carpeta oculta '.venv' en el directorio actual para aislar el proyecto
python3 -m venv .venv

echo -e "\n\e[1;34m=== [3/4] Activando entorno y optimizando PIP ] ===\e[0m"
# Activamos el entorno virtual en la sesión de Bash actual
source .venv/bin/activate

# Actualizamos PIP, setuptools y wheel a las versiones más recientes y estables
pip install --upgrade pip setuptools wheel

echo -e "\n\e[1;34m=== [4/4] Instalando dependencias desde requirements.txt ] ===\e[0m"
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    echo -e "\e[1;33m⚠️ No se encontró requirements.txt. Instalando paquetes por defecto...\e[0m"
    pip install requests pandas
fi

echo -e "\n\e[1;32m======================================================================\e[0m"
echo -e "\e[1;32m   ✅ ¡ENTORNO CONFIGURADO Y DESPLEGADO CON ÉXITO! \e[0m"
echo -e "\e[1;32m======================================================================\e[0m"
echo -e "Para ejecutar tu script de procesamiento del Banco Mundial, haz lo siguiente:"
echo -e "  1) Activa el entorno virtual:  \e[1;33msource .venv/bin/activate\e[0m"
echo -e "  2) Lanza el programa Python:   \e[1;33mpython tu_programa.py\e[0m"
echo -e "  3) Cuando termines, sal con:   \e[1;33mdeactivate\e[0m"
echo -e "======================================================================"