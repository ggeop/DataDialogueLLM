FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the UI code
COPY . .

ENV FLASK_DEBUG=1

# Expose the port for the UI
EXPOSE 5000

# Start the UI service
CMD ["python", "-u", "app.py"]