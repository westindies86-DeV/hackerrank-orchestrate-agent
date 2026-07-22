@echo off
title Claims Audit Agent - 5/5 Valid Demo
color 0A
echo ==========================================
echo  Deterministic Claims Evidence Audit Agent
echo ==========================================
echo.
cd /d "%~dp0"
echo Current folder: %CD%
echo.
echo Checking venv...
if not exist ".\venv\Scripts\python.exe" (
  echo ERROR: venv not found at .\venv\Scripts\python.exe
  echo.
  pause
  exit /b
)
echo venv found OK
echo.
echo Running...
".\venv\Scripts\python.exe" code/main.py
echo.
echo ------------------------------------------
type output.csv
echo ------------------------------------------
echo.
echo DONE. Press any key to close.
pause
