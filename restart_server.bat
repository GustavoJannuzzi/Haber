@echo off
echo ========================================
echo Reiniciando Servidor Streamlit
echo ========================================
echo.

echo [1/4] Parando processos do Streamlit...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq streamlit*" 2>nul
timeout /t 2 >nul

echo [2/4] Limpando cache do Streamlit...
rmdir /S /Q .streamlit 2>nul
del /Q /S __pycache__ 2>nul
del /Q /S *.pyc 2>nul

echo [3/4] Aguardando liberacao de porta...
timeout /t 3 >nul

echo [4/4] Iniciando servidor Streamlit na porta 8501...
python -m streamlit run app.py --server.port 8501

pause
