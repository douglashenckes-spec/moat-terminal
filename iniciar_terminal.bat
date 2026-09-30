@echo off
chcp 65001 > nul
title JP Morgan & Charlie Munger B3 Terminal
cls
echo ===================================================================
echo   🏛️ JP MORGAN ^| CHARLIE MUNGER B3 TERMINAL (CFA RESEARCH)
echo ===================================================================
echo.
echo [1/2] Iniciando servidor analítico e API do Fundamentus...
start "" http://localhost:8050/index.html
python server.py
pause
