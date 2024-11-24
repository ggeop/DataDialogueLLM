import logging
from fastapi import APIRouter
from typing import List
from app.services.models.models import ModelConfig, ModelOption, ModelSource


router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/list", response_model=List[ModelConfig])
async def get_models():
    """
    Return available model configurations
    """
    # TODO: Be dynamic based on Providers APIs
    SUPPORTED_MODELS = [
        ModelConfig(
            source_id=ModelSource.GOOGLE,
            display_name="Google Cloud AI",
            logo_path="/static/images/google-logo.png",
            suggested=True,
            is_local=False,
            options=[
                ModelOption(value="gemini-pro", label="gemini-pro", suggested=True),
                ModelOption(
                    value="gemini-1.5-pro-latest", label="gemini-1.5-pro-latest"
                ),
                ModelOption(value="gemini-1.5-flash", label="gemini-1.5-flash"),
                ModelOption(value="gemini-1.5-flash-8b", label="gemini-1.5-flash-8b"),
                ModelOption(value="custom", label="Custom Model..."),
            ],
        ),
        ModelConfig(
            source_id=ModelSource.OPENAI,
            display_name="OpenAI",
            logo_path="/static/images/openai-logo.png",
            is_local=False,
            options=[
                ModelOption(value="gpt-4o", label="GPT-4o", suggested=True),
                ModelOption(value="gpt-4o-mini", label="GPT-4o mini"),
                ModelOption(value="gpt-4-turbo", label="GPT-4 turbo"),
                ModelOption(value="gpt-4", label="GPT-4"),
                ModelOption(value="gpt-3.5-turbo", label="GPT-3.5 turbo"),
            ],
        ),
        ModelConfig(
            source_id=ModelSource.HUGGINGFACE,
            display_name="Hugging Face",
            logo_path="/static/images/hf-logo.png",
            is_local=True,
            options=[
                ModelOption(
                    repo_id="lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF",
                    value="meta-llama-3.1-8b-instruct-q8_0",
                    label="Meta-Llama-3.1-8B-Instruct-Q8_0",
                    size="8.54GB",
                ),
                ModelOption(
                    repo_id="lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF",
                    value="meta-llama-3.1-8b-instruct-q6_k",
                    label="Meta-Llama-3.1-8B-Instruct-Q6_K",
                    size="6.60GB",
                ),
                ModelOption(
                    repo_id="lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF",
                    value="meta-llama-3.1-8b-instruct-q5_k_m",
                    label="Meta-Llama-3.1-8B-Instruct-Q5_K_M",
                    size="5.73GB",
                ),
            ],
        ),
    ]
    return SUPPORTED_MODELS
