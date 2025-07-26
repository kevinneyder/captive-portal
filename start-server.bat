@echo off
title Portal Cautivo Restaurante
cd /d %~dp0

echo Iniciando servidor de encuestas...
echo Accesible en: http://%COMPUTERNAME%.local:5000/

start python app.py

echo Servidor iniciado. Mantenga esta ventana abierta.
pause