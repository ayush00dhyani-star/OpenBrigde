@echo off
REM OpenBridge Windows Installer
REM The absolute easiest way to install OpenBridge on Windows

setlocal enabledelayedexpansion

:: Set colors (ANSI escape codes)
set "BLUE=[94m"
set "GREEN=[92m"
set "YELLOW=[93m"
set "RED=[91m"
set "NC=[0m"

:: Title
echo.
echo ╔══════════════════════════════════════════════════════╗
echo ║        OPENBRIDGE WINDOWS INSTALLER                  ║
echo ╚══════════════════════════════════════════════════════╝
echo.

:: Check if running in correct directory
if not exist "requirements.txt" (
    echo %RED%❌ Please run this script from the OpenBridge directory%NC%
    echo %YELLOW%ℹ️  Usage: cd openbridge ^&^& install.bat%NC%
    pause
    exit /b 1
)

:: Step 1: Check Python
echo %YELLOW%ℹ️  Checking Python installation...%NC%
python --version >nul 2>&1
if %errorlevel% neq 0 (
    py --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo %RED%❌ Python not found!%NC%
        echo.
        echo %YELLOW%ℹ️  Python 3.10+ is required. Would you like to download it?%NC%
        echo.
        set /p choice="Open Python download page? (Y/n): "
        if /i not "!choice!"=="n" (
            start https://www.python.org/downloads/
            echo.
            echo %YELLOW%ℹ️  After installing Python, please run this script again.%NC%
            echo %YELLOW%ℹ️  Make sure to check 'Add Python to PATH' during installation!%NC%
            pause
            exit /b 1
        ) else (
            echo %RED%❌ Installation cannot continue without Python.%NC%
            pause
            exit /b 1
        )
    ) else {
        set PYTHON_CMD=py
        for /f "tokens=2" %%i in ('py --version 2^>^&1') do set PYTHON_VERSION=%%i
        echo %GREEN%✅ Found Python !PYTHON_VERSION!%NC%
    }
) else {
    set PYTHON_CMD=python
    for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
    echo %GREEN%✅ Found Python !PYTHON_VERSION!%NC%
}

:: Verify Python version
for /f "tokens=2 delims=." %%a in ("!PYTHON_VERSION!") do set PY_MINOR=%%a
if !PY_MINOR! LSS 10 (
    echo %RED%❌ Python 3.10+ is required. You have Python 3.!PY_MINOR!%NC%
    echo %YELLOW%ℹ️  Please upgrade Python from https://python.org/downloads%NC%
    pause
    exit /b 1
)

:: Step 2: Create virtual environment
echo.
echo %YELLOW%ℹ️  Setting up virtual environment...%NC%
if not exist "venv" (
    %PYTHON_CMD% -m venv venv
    echo %GREEN%✅ Virtual environment created%NC%
) else (
    echo %GREEN%✅ Virtual environment already exists%NC%
)

:: Activate virtual environment
call venv\Scripts\activate.bat

:: Step 3: Upgrade pip
echo.
echo %YELLOW%ℹ️  Upgrading pip...%NC%
python -m pip install --upgrade pip --quiet
echo %GREEN%✅ Pip upgraded%NC%

:: Step 4: Install dependencies
echo.
echo %YELLOW%ℹ️  Installing Python packages (this may take a few minutes)...%NC%
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo %RED%❌ Failed to install dependencies%NC%
    pause
    exit /b 1
)
echo %GREEN%✅ Dependencies installed%NC%

:: Step 5: Install browser
echo.
echo %YELLOW%ℹ️  Installing Chromium browser (this may take a few minutes)...%NC%
playwright install chromium
if %errorlevel% neq 0 (
    echo %YELLOW%⚠️  Browser installation had issues, but you can retry later with: playwright install chromium%NC%
) else (
    echo %GREEN%✅ Browser installed%NC%
)

:: Step 6: Create directories
echo.
echo %YELLOW%ℹ️  Creating directories...%NC%
if not exist "logs" mkdir logs
if not exist "sessions" mkdir sessions
if not exist "data" mkdir data
echo %GREEN%✅ Directories created%NC%

:: Step 7: Setup config
if not exist "config.yaml" (
    echo.
    echo %YELLOW%ℹ️  Creating configuration file...%NC%
    copy config.example.yaml config.yaml >nul
    echo %GREEN%✅ Configuration file created%NC%
    echo %YELLOW%ℹ️  Edit config.yaml to set your channel name%NC%
) else (
    echo.
    echo %GREEN%✅ Configuration file already exists%NC%
)

:: Step 8: Optional wizard
echo.
set /p run_wizard="Would you like to run the setup wizard now? (Y/n): "
if /i not "!run_wizard!"=="n" (
    echo.
    echo %YELLOW%ℹ️  Starting setup wizard...%NC%
    python wizard.py
) else (
    echo.
    echo %YELLOW%ℹ️  You can run the wizard later with: python wizard.py%NC%
    echo %YELLOW%ℹ️  Or start OpenBridge with: start.bat%NC%
)

:: Show completion message
echo.
echo ╔══════════════════════════════════════════════════════╗
echo ║           INSTALLATION COMPLETE!                     ║
echo ╚══════════════════════════════════════════════════════╝
echo.
echo %GREEN%Next steps:%NC%
echo   1. Edit config.yaml to set your channel name
echo   2. Run start.bat to launch OpenBridge
echo   3. Log into Twitch when the browser opens
echo   4. Go live and let OpenBridge handle the rest!
echo.
echo %YELLOW%Quick commands:%NC%
echo   start.bat         - Interactive menu
echo   python wizard.py  - Setup wizard
echo   python main.py    - Start directly
echo.

pause
