#!/bin/bash

set -e

echo "Creando entorno virtual .env..."
python3 -m venv .env

echo "Actualizando pip..."
.env/bin/python -m pip install --upgrade pip

echo "Instalando pandas y numpy..."
.env/bin/python -m pip install pandas numpy

echo "Entorno virtual creado correctamente."
echo "Para activarlo, ejecuta: source .env/bin/activate"