import os
from huggingface_hub import hf_hub_download


def download_model():

    MODEL_REPO = os.getenv('MODEL_REPO')
    if not MODEL_REPO:
        raise ValueError("MODEL_REPO environment variable is not set or is empty")

    MODEL_FILE = os.getenv('MODEL_FILE')
    if not MODEL_FILE:
        raise ValueError("MODEL_FILE environment variable is not set or is empty")

    MODEL_LOCAL_DIR = os.getenv('MODEL_LOCAL_DIR')
    if not MODEL_LOCAL_DIR:
        raise ValueError("MODEL_LOCAL_DIR environment variable is not set or is empty")

    hf_hub_download(
        repo_id=MODEL_REPO,
        filename=MODEL_FILE,
        local_dir=MODEL_LOCAL_DIR
    )


if __name__ == "__main__":
    download_model()
