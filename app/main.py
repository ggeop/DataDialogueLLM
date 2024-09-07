from fastapi import FastAPI
from pydantic import BaseModel
from llama_cpp import Llama
import os

app = FastAPI()

print

# Get the model path
model_path = "/root/.cache/huggingface/hub/models--lmstudio-community--Meta-Llama-3.1-8B-Instruct-GGUF/snapshots/8601e6db71269a2b12255ebdf09ab75becf22cc8/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf"
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model file not found at {model_path}")

# Load the model
model = Llama(model_path=model_path)

class Query(BaseModel):
    text: str

@app.post("/generate")
async def generate_text(query: Query):
    prompt = f"Human: {query.text}\n\nAssistant:"
    response = model(prompt, max_tokens=100, stop=["Human:", "\n"], echo=True)
    return {"response": response['choices'][0]['text'].split("Assistant:")[-1].strip()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)