@echo off
echo Setting up Black code formatter...

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed! Please install Python first.
    exit /b 1
)

:: Create virtual environment if it doesn't exist
if not exist "backend\venv" (
    echo Creating virtual environment...
    python -m venv backend\venv
)

:: Activate virtual environment
call backend\venv\Scripts\activate

:: Install requirements
echo Installing Black and pre-commit...
python -m pip install --upgrade pip
python -m pip install black
python -m pip install pre-commit

:: Initialize pre-commit
echo Setting up pre-commit...
pre-commit install

echo Setup complete! You can now run 'black backend' to format your code.
echo To format code automatically before each commit, pre-commit is now installed.