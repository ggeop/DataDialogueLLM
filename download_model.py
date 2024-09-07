from huggingface_hub import hf_hub_download

def download_model():
    model_path = hf_hub_download(repo_id="lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF", filename="Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf")
    print(f"Model downloaded to: {model_path}")

if __name__ == "__main__":
    download_model()