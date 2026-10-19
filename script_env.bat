@echo off
setlocal

echo Creando entorno virtual .env...
python -m venv .env
if errorlevel 1 goto error

echo Actualizando pip...
.env\Scripts\python.exe -m pip install --upgrade pip
if errorlevel 1 goto error

echo Instalando pandas y numpy...
.env\Scripts\python.exe -m pip install pandas numpy
if errorlevel 1 goto error

echo.
echo Entorno virtual creado correctamente.
echo Para activarlo, ejecuta: .env\Scripts\activate
goto fin

:error
echo.
echo ERROR: No se pudo completar la creacion del entorno.
echo Comprueba que Python esta instalado y disponible en PATH.
exit /b 1

:fin
endlocal
