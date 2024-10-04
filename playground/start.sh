#!/bin/bash

if [ ! -f /data/model/$MODEL_NAME ]; then
    echo "Model $MODEL_NAME not found in /data/model/"
    echo "Downloading $MODEL_NAME from $HF_REPO..."
    python -c "from huggingface_hub import hf_hub_download; hf_hub_download('$HF_REPO', '$MODEL_NAME', local_dir='/data/model')"
    echo "Download complete."
else
    echo "Model $MODEL_NAME found in /data/model/"
fi

echo "Starting Jupyter Notebook..."
jupyter notebook --ip='0.0.0.0' --port=8888 --no-browser --allow-root --notebook-dir=/data/notebooks