# Local Development Setup Guide

## Prerequisites

- Python 3.7 or higher
- Git
- Docker and Docker Compose (optional, for container development)

## Project Structure Update
```
data-dialogue/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── services/
│   │   └── main.py
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
├── scripts/
│   └── black/
│       ├── setup_linux.sh
│       └── setup_windows.bat
├── docker-compose.yml
├── pyproject.toml
├── .pre-commit-config.yaml
├── .gitignore
└── README.md
```

## Code Style Setup

We use Black for code formatting to maintain consistent code style across the project. The setup scripts are provided for both Windows and Linux environments.

### Windows Setup

1. Open Command Prompt as administrator
2. Navigate to your project directory:
   ```batch
   cd path\to\data-dialogue
   ```
3. Run the setup script:
   ```batch
   scripts\black\setup_windows.bat
   ```

### Linux Setup

1. Open terminal
2. Navigate to your project directory:
   ```bash
   cd path/to/data-dialogue
   ```
3. Make the script executable:
   ```bash
   chmod +x scripts/black/setup_linux.sh
   ```
4. Run the setup script:
   ```bash
   ./scripts/black/setup_linux.sh
   ```

### Manual Code Formatting

After setup, you can use the following commands:

```bash
# Format all Python files in backend
black backend

# Check formatting without making changes
black backend --check

# Show what changes would be made
black backend --diff

# Format a specific file
black backend/app/main.py
```

### Pre-commit Hooks

The setup scripts install pre-commit hooks that automatically format your code before each commit. To manually run all pre-commit checks:
```bash
pre-commit run --all-files
```

## Local Development Environment

### Backend Setup

1. Create and activate virtual environment:

   **Windows:**
   ```batch
   cd backend
   python -m venv venv
   venv\Scripts\activate
   ```

   **Linux:**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running Services Locally

#### Using Docker Compose (Recommended for full stack):
```bash
docker-compose up try-demo-db-local backend-local frontend-local --build
```

#### Running Services Individually:

1. Backend:
   ```bash
   cd backend
   python app/main.py
   ```
   The backend will be available at `http://localhost:8000`

2. Frontend:
   Refer to frontend documentation for specific setup instructions.

## Configuration

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Update the `.env` file with your specific configuration values

## Common Issues

### Black Setup Troubleshooting

1. If you encounter permission issues:
   - Windows: Run Command Prompt as administrator
   - Linux: Use `sudo` for permissions

2. Virtual Environment Issues:
   - Ensure Python is in your system PATH
   - Try creating the virtual environment manually if the script fails

### Development Environment Issues

1. Port Conflicts:
   - Check if ports 8000 (backend) or 5000 (frontend) are already in use
   - Modify the port numbers in your configuration if needed

2. Database Connectivity:
   - Ensure the demo database is running if using local development
   - Check database credentials in your `.env` file

## Contributing

Before submitting a pull request:
1. Ensure all code is formatted with Black
2. Run pre-commit checks
3. Write or update tests as needed
4. Follow the [Contributing Guidelines](./CONTRIBUTING.md)

## Additional Resources

- [Black Documentation](https://black.readthedocs.io/en/stable/)
- [Pre-commit Documentation](https://pre-commit.com/)
- [Project README](./README.md)
