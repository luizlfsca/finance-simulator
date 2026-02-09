@echo off
echo --- Configurando Ambiente do Simulador ---
echo Instalando dependencias (pode demorar um pouco)...
"C:\Users\lzfel\AppData\Local\Programs\Python\Python312\python.exe" -m pip install streamlit pandas matplotlib

echo.
echo --- Iniciando Simulador Financeiro ---
"C:\Users\lzfel\AppData\Local\Programs\Python\Python312\python.exe" -m streamlit run app.py
pause
