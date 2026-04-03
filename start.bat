@echo off
REM OpenBridge Windows Quick Start
REM The absolute easiest way to start OpenBridge on Windows

setlocal enabledelayedexpansion

:: Title
echo.
echo ╔══════════════════════════════════════════════════════╗
echo ║        OPENBRIDGE QUICK START                        ║
echo ╚══════════════════════════════════════════════════════╝
echo.

:: Check if running in correct directory
if not exist "requirements.txt" (
    echo [91m❌ Please run this script from the OpenBridge directory[0m
    echo [93mℹ️  Usage: cd openbridge ^&^& start.bat[0m
    pause
    exit /b 1
)

:: Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    py --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo [91m❌ Python not found![0m
        echo.
        echo [93mℹ️  Please run install.bat first to set up OpenBridge[0m
        echo.
        pause
        exit /b 1
    )
    set PYTHON_CMD=py
) else {
    set PYTHON_CMD=python
}

:: Check if config exists
if not exist "config.yaml" (
    echo [93mℹ️  No configuration found. Starting setup wizard...[0m
    echo.
    %PYTHON_CMD% wizard.py
    exit /b %errorlevel%
)

:: Config exists, show menu
echo [92m✅ Configuration found![0m
echo.
echo What would you like to do?
echo   1. Start OpenBridge
echo   2. Re-run setup wizard
echo   3. View current configuration
echo   4. Exit
echo.
set /p choice="Enter choice (1-4) [1]: "
if "!choice!"=="" set choice=1

if "!choice!"=="1" (
    echo.
    echo [92m🚀 Starting OpenBridge...[0m
    echo.
    %PYTHON_CMD% main.py
) else if "!choice!"=="2" (
    echo.
    %PYTHON_CMD% wizard.py
) else if "!choice!"=="3" (
    echo.
    echo ============================================================
    type config.yaml
    echo ============================================================
    echo.
    pause
    goto :menu
) else if "!choice!"=="4" (
    echo.
    echo 👋 Goodbye!
    exit /b 0
) else (
    echo Invalid choice. Exiting.
    exit /b 1
)

:menu
