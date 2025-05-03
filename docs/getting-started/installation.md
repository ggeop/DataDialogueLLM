# Installation Guide

This guide will help you get DataDialogue up and running on your system.

## Prerequisites

Before installing DataDialogue, make sure you have the following prerequisites installed:

- Docker (version 20.10.0 or higher)
- Docker Compose (version 2.0.0 or higher)
- Git

## Installation Methods

### Method 1: Using Docker (Recommended)

The easiest way to get started with DataDialogue is using Docker:

```bash
# Clone the repository
git clone https://github.com/yourusername/DataDialogue

# Navigate to the project directory
cd DataDialogue

# Start the application
docker-compose up
```

The application will be available at `http://localhost:3000`.

### Method 2: Manual Installation

If you prefer to run the application without Docker, follow these steps:

#### Backend Setup

```bash
# Navigate to the backend directory
cd backend

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
.\venv\Scripts\activate
# On Unix or MacOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the backend server
python main.py
```

#### Frontend Setup

```bash
# Navigate to the frontend directory
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

## Configuration

After installation, you might want to configure:

1. Environment variables (copy `.env.example` to `.env`)
2. Database settings
3. API endpoints


## Verifying Installation

To verify that DataDialogue is running correctly:

1. Open your browser and navigate to `http://localhost:3000`
2. You should see the DataDialogue landing page
3. Try uploading a sample dataset to test the functionality

## Troubleshooting

If you encounter any issues during installation:

1. Check if all prerequisites are installed correctly
2. Ensure all ports (3000 for frontend, 8000 for backend) are available
3. Check the logs using `docker-compose logs`
4. Refer to our [GitHub Issues](https://github.com/yourusername/DataDialogue/issues) page

## Next Steps

- Follow our [Quick Start Guide](../getting-started/quick-start.md) to begin using DataDialogue
- Join our community and [contribute](../community/CONTRIBUTING.md) to the project 