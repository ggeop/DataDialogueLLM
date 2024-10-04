FROM python:3.9

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables for model download
ARG MODEL_REPO
ARG MODEL_FILE
ARG MODEL_LOCAL_DIR
ENV MODEL_REPO=${MODEL_REPO}
ENV MODEL_FILE=${MODEL_FILE}
ENV MODEL_LOCAL_DIR=${MODEL_LOCAL_DIR}

# Copy only the necessary files for model download
COPY app/core/config.py app/core/config.py
COPY app/utils/download_model.py app/utils/download_model.py

# Run the download script
RUN python -m app.utils.download_model

RUN pip install nltk
RUN python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab'); nltk.download('stopwords')"



# Copy the rest of the application
COPY . .

# Set Python path
ENV PYTHONPATH=/app


# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]