@echo off
setlocal enabledelayedexpansion

:: Enable the code page to UTF-8, which should now allow the emojis
chcp 65001

echo ==========================================
echo 🚀 Data Dialogue Dev Local Setup 🚀 
echo ==========================================

:: Set specific Python 3.12 installation directory
set PYTHON_DIR=%LOCALAPPDATA%\Programs\Python\Python312
set PYTHON_PATH=%PYTHON_DIR%\python.exe

echo 🔍 Checking Python 3.12 installation...

:: Check if Python 3.12 is already installed in the specified directory
if exist "%PYTHON_PATH%" (
    echo ✅ Python 3.12 is already installed at %PYTHON_DIR%
) else (
    echo 📥 Installing Python 3.12 to custom directory...
    
    :: Download Python 3.12 installer
    echo ⬇️ Downloading Python 3.12 installer...
    powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.12.2/python-3.12.2-amd64.exe' -OutFile 'python-3.12.2-amd64.exe'"
    
    :: Install Python 3.12 silently to custom directory without registering as default Python
    echo 🛠️ Installing Python 3.12...
    start /wait python-3.12.2-amd64.exe /quiet TargetDir=%PYTHON_DIR% Include_test=0 ^
        AssociateFiles=0 PrependPath=0 Include_launcher=0 InstallLauncherAllUsers=0
    
    :: Delete the installer
    del python-3.12.2-amd64.exe
    
    :: Verify installation
    if not exist "%PYTHON_PATH%" (
        echo ❌ Failed to install Python 3.12. Please install it manually from https://www.python.org/downloads/
        exit /b 1

    )
)

echo 🚀 Setting up Black code formatter and Commitizen...

:: Create virtual environment if it doesn't exist using specific Python 3.12
if not exist "backend\venv" (
    echo 🔧 Creating virtual environment with Python 3.12...
    "%PYTHON_PATH%" -m venv backend\venv
)

:: Activate virtual environment
call backend\venv\Scripts\activate

:: Install requirements
echo 📦 Installing required packages...
python -m pip install -r .\scripts\requirements.txt

:: Initialize pre-commit
echo Setting up pre-commit...
:: Unset the existing hooks path
git config --unset-all core.hooksPath
:: Clean any existing pre-commit installations
echo ⚙️ Setting up pre-commit...
pre-commit clean
pre-commit uninstall
:: Install the new pre-commit hooks
pre-commit install
pre-commit install --hook-type commit-msg
echo.
echo ================================
echo Setup complete!🚀 
echo ================================
echo The following has been set up:
echo ✅ Python 3.12 installation checked/completed
echo 🌟 Virtual environment created/updated
echo ⚡ Black code formatter installed 
echo 🔗 Pre-commit hooks installed
echo 📝 Commitizen installed for commit message formatting