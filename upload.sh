#!/bin/bash

# Mensaje de espera (corregido a 5 segundos reales con -t 5 si es lo que buscas, o -t 2 como tenías)
read -rsp $'Presione cualquier tecla para continuar o espere... \n' -n 1 -t 2;
echo -e "\nIniciando proceso de sincronización..."

# 1. Definir variables para fecha y tiempo (Formato: Año_Mes_Día_Hora_Min_Seg)
date_stamp=$(date +"%Y_%m_%d_%H_%M_%S")

# 2. Agregar todos los cambios al área de preparación (Staging)
echo "=> Ejecutando: git add ."
git add .

# 3. Crear el commit local con la marca de tiempo. 
# Añadimos un validador: si no hay cambios nuevos, el script no falla.
echo "=> Ejecutando: git commit"
git commit -m "Auto-backup: $date_stamp" || echo "No hay cambios nuevos para commitear."

# 4. Asegurar que estamos en la rama main
echo "=> Asegurando rama main"
git branch -M main

# 5. Traer cambios remotos de forma segura ANTES del push.
# --rebase evita que se creen commits de merge innecesarios y mantiene el historial limpio.
echo "=> Ejecutando: git pull --rebase origin main"
git pull --rebase origin main

# 6. Subir los cambios a GitHub
echo "=> Ejecutando: git push -u origin main"
git push -u origin main

echo "¡Todo sincronizado con éxito para el taller!"