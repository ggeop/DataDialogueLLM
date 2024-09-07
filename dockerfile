FROM python:3.9

WORKDIR /app

# Install system dependencies
# RUN apt-get update && apt-get install -y \
#     build-essential \
#     git \
#     && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# Download the model
COPY download_model.py .
RUN python download_model.py

## Copy the application code
COPY app app

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["python", "app/main.py"]