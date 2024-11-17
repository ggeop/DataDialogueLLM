#!/bin/bash

echo "Setting up Black code formatter..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python is not installed! Please install Python first."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "backend/venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv backend/venv
fi

# Activate virtual environment
source backend/venv/bin/activate

# Install requirements
echo "Installing Black and pre-commit..."
python -m pip install --upgrade pip
python -m pip install black
python -m pip install pre-commit

# Initialize pre-commit
echo "Setting up pre-commit..."
pre-commit install

# Make sure the script is executable
chmod +x scripts/setup_black_linux.sh

echo "Setup complete! You can now run 'black backend' to format your code."
echo "To format code automatically before each commit, pre-commit is now installed."