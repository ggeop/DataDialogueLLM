# Data Dialogue

Data Dialogue is an application that creates prompts, retrieves data from various sources, and generates responses using an LLM backend. The application runs in Docker and consists of two main services: the LLM backend and the UI.

## Project Structure

```
data-dialogue/
   ├── backend/
   │   ├── app/
   │   │   ├── api/
   │   │   │   ├── __init__.py
   │   │   │   ├── endpoints.py
   │   │   │   └── models.py
   │   │   ├── core/
   │   │   │   ├── __init__.py
   │   │   │   ├── config.py
   │   │   │   └── logging.py
   │   │   ├── services/
   │   │   │   ├── __init__.py
   │   │   │   └── llm_service.py
   │   │   └── main.py
   │   ├── Dockerfile
   │   └── requirements.txt
   ├── frontend/
   │   ├── static/
   │   │   ├── css/
   │   |   |    └── style.css
   │   │   ├── images/
   │   |   |    └── ...
   │   │   ├── js/
   │   |   |    └── script.js
   │   │   ├── templates/
   │   |   |    └── index.html
   │   │   └── app.py
   │   └── Dockerfile
   ├── docker-compose.yml
   ├── .gitignore
   ├── .env.example
   └── README.md
```

## Installation and Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/data-dialogue.git
   cd data-dialogue
   ```

2. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Fill in the required environment variables

3. Build and run the Docker containers:
   ```
   docker-compose up --build
   ```

4. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000

--- 
## Development

This document provides instructions for building the Data Dialogue project.\
It covers building the backend and frontend separately, as well as building the entire project using docker-compose.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Building the Backend](#building-the-backend)
3. [Building the Frontend](#building-the-frontend)
4. [Building with Docker Compose](#building-with-docker-compose)
5. [Running the Application](#running-the-application)
6. [Troubleshooting](#troubleshooting)

## Prerequisites

Ensure you have the following installed:
- Docker
- Docker Compose
- Node.js and npm (for local frontend development)
- Python 3.9 (for local backend development)

## Building the Backend

## Building with Docker Compose

Docker Compose allows you to build and run both the backend and frontend together.

1. Ensure you're in the project root directory where the `docker-compose.yml` file is located.

2. Build and Run
```
docker-compose up --build
```

This will start both the backend and frontend services. The frontend will be available at `http://localhost:3000`, and the backend at `http://localhost:8000`.

## Running the Application

After building with Docker Compose:

1. Access the frontend at `http://localhost:5000` in your web browser.
2. The frontend will communicate with the backend at `http://localhost:8000`.

For local development:
- Run the backend and frontend in separate terminal windows using the local development instructions above.
- Ensure the `LLM_BACKEND_URL` in your frontend `.env` file is set to `http://localhost:8000/generate`.

## Troubleshooting

1. **Backend build fails**: 
   - Ensure the `.env` file exists and contains the correct `MODEL_REPO` and `MODEL_FILE` values.
   - Check internet connection for model download.

3. **Docker Compose issues**:
   - Ensure Docker and Docker Compose are up to date.
   - Check if ports 3000 and 8000 are free on your machine.

4. **Backend and Frontend can't communicate**:
   - Check the `LLM_BACKEND_URL` in the frontend `.env` file.
   - Ensure your firewall isn't blocking the communication.

For any other issues, check the application logs using `docker-compose logs` or the individual service logs.
