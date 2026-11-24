@echo off
chcp 65001 >nul
title PDM Abrantes - processar
cd /d "%~dp0"
set PY=
where py >nul 2>nul && set PY=py
if not defined PY (where python >nul 2>nul && set PY=python)
if not defined PY (
  echo.
  echo Falta o Python. Instala em https://www.python.org/downloads/
  echo e marca a opcao "Add python.exe to PATH". Depois volta a abrir este ficheiro.
  pause
  exit /b
)
echo A preparar (so demora na primeira vez)...
%PY% -m pip install --quiet --disable-pip-version-check geopandas matplotlib
%PY% scripts\processar.py %1
echo.
pause
