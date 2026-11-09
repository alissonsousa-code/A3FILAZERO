@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo Criando ambiente virtual...
  py -m venv .venv
)
call ".venv\Scripts\activate.bat"
echo Instalando dependencias do FilaZero...
python -m pip install -r requirements.txt
if errorlevel 1 (
  echo.
  echo Nao foi possivel instalar as dependencias. Verifique sua conexao com a internet.
  pause
  exit /b 1
)
echo.
echo Iniciando FilaZero em http://127.0.0.1:5000
python app.py
pause
