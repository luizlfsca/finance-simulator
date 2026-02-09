@echo off
echo --- Instalando Plotly (necessario para graficos interativos) ---
"C:\Users\lzfel\AppData\Local\Programs\Python\Python312\python.exe" -m pip install plotly
echo.
echo --- Iniciando Simulador Financeiro TURBINADO ---
"C:\Users\lzfel\AppData\Local\Programs\Python\Python312\python.exe" -m streamlit run app.py
pause
