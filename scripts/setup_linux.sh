#!/bin/bash

# Enable UTF-8 encoding for emojis
export LANG=en_US.UTF-8

echo "=========================================="
echo "🚀 Data Dialogue Dev Local Setup 🚀"
echo "=========================================="

# Set specific Python 3.12 installation directory
PYTHON_DIR="$HOME/.local/python312"
PYTHON_PATH="$PYTHON_DIR/bin/python3"

echo "🔍 Checking Python 3.12 installation..."

# Check if Python 3.12 is already installed in the specified directory
if [ -f "$PYTHON_PATH" ]; then
    echo "✅ Python 3.12 is already installed at $PYTHON_DIR"
else
    echo "📥 Installing Python 3.12 to custom directory..."
    
    # Install build dependencies
    echo "⚙️ Installing build dependencies..."
    if command -v apt-get &> /dev/null; then
        sudo apt-get update
        sudo apt-get install -y wget build-essential libssl-dev zlib1g-dev \
            libbz2-dev libreadline-dev libsqlite3-dev curl \
            libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev \
            libffi-dev liblzma-dev
    elif command -v dnf &> /dev/null; then
        sudo dnf groupinstall -y "Development Tools"
        sudo dnf install -y wget openssl-devel bzip2-devel libffi-devel \
            xz-devel readline-devel sqlite-devel zlib-devel
    elif command -v pacman &> /dev/null; then
        sudo pacman -Sy --noconfirm base-devel openssl zlib readline sqlite curl
    else
        echo "❌ Unsupported package manager. Please install build dependencies manually."
        exit 1
    fi
    
    # Create temporary directory for building
    BUILD_DIR=$(mktemp -d)
    cd "$BUILD_DIR"
    
    # Download and extract Python 3.12
    echo "⬇️ Downloading Python 3.12 source..."
    wget https://www.python.org/ftp/python/3.12.2/Python-3.12.2.tgz
    tar xzf Python-3.12.2.tgz
    cd Python-3.12.2
    
    # Configure and build Python
    echo "🛠️ Building Python 3.12..."
    ./configure --prefix="$PYTHON_DIR" --enable-optimizations
    make -j$(nproc)
    make install
    
    # Clean up build directory
    cd
    rm -rf "$BUILD_DIR"
    
    # Verify installation
    if [ ! -f "$PYTHON_PATH" ]; then
        echo "❌ Failed to install Python 3.12. Please install it manually from python.org"
        exit 1
    fi
fi

echo "🚀 Setting up Black code formatter and Commitizen..."

# Create virtual environment if it doesn't exist using specific Python 3.12
if [ ! -d "backend/venv" ]; then
    echo "🔧 Creating virtual environment with Python 3.12..."
    "$PYTHON_PATH" -m venv backend/venv
fi

# Activate virtual environment
source backend/venv/bin/activate

# Install requirements
echo "📦 Installing required packages..."
python -m pip install -r ./scripts/requirements.txt

# Initialize pre-commit
echo "⚙️ Setting up pre-commit..."
# Unset the existing hooks path
git config --unset-all core.hooksPath
# Clean any existing pre-commit installations
pre-commit clean
pre-commit uninstall
# Install the new pre-commit hooks
pre-commit install
pre-commit install --hook-type commit-msg

echo
echo "================================"
echo "Setup complete! 🚀"
echo "================================"
echo "The following has been set up:"
echo "✅ Python 3.12 installation checked/completed"
echo "🌟 Virtual environment created/updated"
echo "⚡ Black code formatter installed"
echo "🔗 Pre-commit hooks installed"
echo "📝 Commitizen installed for commit message formatting"