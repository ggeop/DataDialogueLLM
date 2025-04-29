# Local Development Setup Guide

## Prerequisites

- Git
- Docker and Docker Compose (optional, for container development)

## Setup

For local development we need to setup few packages in our local machine. The installation is handled by one script.

### Windows Setup

1. Open Command Prompt as administrator
2. Navigate to your project directory:
   ```batch
   cd path\to\data-dialogue
   ```
3. Run the setup script:
   ```batch
   scripts\setup_windows.bat
   ```

### Linux Setup

1. Open terminal
2. Navigate to your project directory:
   ```bash
   cd path/to/data-dialogue
   ```
3. Make the script executable:
   ```bash
   chmod +x scripts/setup_linux.sh
   ```

4. Run the setup script:

   *If you are using linux subsystem (e.g wsl) Run this command first:*
   ```bash
   sudo apt-get install dos2unix  # Install if not present
   dos2unix scripts/setup_linux.sh
   ```

   ```bash
   ./scripts/setup_linux.sh
   ```

### Running Services Locally

#### Using Docker Compose (Recommended for full stack):
```bash
docker-compose up --build
```