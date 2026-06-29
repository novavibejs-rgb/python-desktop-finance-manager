@echo off
REM Script para executar o Gerenciador de Despesas no Windows

title Gerenciador de Despesas e Vales

REM Verifica se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo [ERRO] Python não encontrado!
    echo.
    echo Para usar este programa, você precisa ter Python instalado.
    echo Baixe em: https://www.python.org/downloads/
    echo.
    echo Certifique-se de marcar a opção "Add Python to PATH" durante a instalação.
    echo.
    pause
    exit /b 1
)

REM Verifica se Tkinter está disponível
python -m tkinter >nul 2>&1
if errorlevel 1 (
    echo.
    echo [AVISO] Tkinter pode não estar instalado corretamente.
    echo.
    echo Reinstale Python e certifique-se de marcar:
    echo   - tcl/tk and IDLE
    echo.
)

REM Executa o programa
echo.
echo Iniciando Gerenciador de Despesas...
echo.

python main.py

if errorlevel 1 (
    echo.
    echo [ERRO] Erro ao executar o programa.
    echo.
    pause
    exit /b 1
)
