
FROM python:3.9

WORKDIR /app

RUN pip install jupyter huggingface_hub==0.24.7 llama_cpp_python==0.2.90

# Set environment variables for Hugging Face, repository, and model name
ENV HF_HOME=/data/.cache/huggingface
ENV HF_REPO=lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF
ENV MODEL_NAME=Meta-Llama-3.1-8B-Instruct-Q8_0.gguf

# Create a jupyter_notebook_config.py file
# Modify the Jupyter configuration to disable authentication
RUN jupyter notebook --generate-config
RUN echo "c.NotebookApp.token = ''" >> /root/.jupyter/jupyter_notebook_config.py && \
    echo "c.NotebookApp.password = ''" >> /root/.jupyter/jupyter_notebook_config.py

EXPOSE 8888

COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

CMD ["/app/start.sh"]
