@echo off
chcp 65001 >nul
title PDM Abrantes - processar
cd /d "%~dp0"
set PYTHONUTF8=1
set PY=
where py >nul 2>nul && set PY=py
if defined PY goto temos
where python >nul 2>nul && set PY=python
if defined PY goto temos
for %%F in ("%LOCALAPPDATA%\Microsoft\WindowsApps\python3.exe" "%LOCALAPPDATA%\Microsoft\WindowsApps\python.exe") do if exist %%F if not defined PY set PY="%%~F"
if defined PY goto temos
for /d %%D in ("%LOCALAPPDATA%\Programs\Python\Python3*") do if exist "%%D\python.exe" set PY="%%D\python.exe"
if defined PY goto temos
echo.
echo Falta o Python. Instala o Python 3.12 pela Microsoft Store ou pelo Company Portal
echo e depois volta a abrir este ficheiro.
pause
exit /b

:temos
echo A usar o Python: %PY%
echo A preparar - so demora na primeira vez...
%PY% -m pip install --user --quiet --disable-pip-version-check geopandas matplotlib
%PY% scripts\processar.py %1
