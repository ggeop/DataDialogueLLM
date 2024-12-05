import logging
from fastapi import APIRouter
from typing import List
from app.services.models.models import ModelConfig, ModelOption, ModelProvider


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
            source_id=ModelProvider.GOOGLE,
            display_name="Google Cloud AI",
            logo_path="/static/images/logos/google-logo.png",
            suggested=True,
            is_local=False,
            has_token=True,
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
            source_id=ModelProvider.OPENAI,
            display_name="OpenAI",
            logo_path="/static/images/logos/openai-logo.png",
            is_local=False,
            has_token=True,
            options=[
                ModelOption(value="gpt-4o", label="GPT-4o", suggested=True),
                ModelOption(value="gpt-4o-mini", label="GPT-4o mini"),
                ModelOption(value="gpt-4-turbo", label="GPT-4 turbo"),
                ModelOption(value="gpt-4", label="GPT-4"),
                ModelOption(value="gpt-3.5-turbo", label="GPT-3.5 turbo"),
            ],
        ),
        ModelConfig(
            source_id=ModelProvider.ANTHROPIC,
            display_name="Anthropic",
            logo_path="/static/images/logos/anthropic-ai-logo.png",
            is_local=False,
            has_token=True,
            options=[
                ModelOption(
                    value="claude-3-5-sonnet-latest",
                    label="Claude 3.5 Sonnet",
                    suggested=True,
                ),
                ModelOption(value="claude-3-5-haiku-latest", label="Claude 3.5 Haiku"),
                ModelOption(value="claude-3-opus-latest", label="Claude 3 Opus"),
            ],
        ),
        ModelConfig(
            source_id=ModelProvider.HUGGINGFACE,
            display_name="Hugging Face (.gguf)",
            logo_path="/static/images/logos/hf-logo.png",
            is_local=True,
            options=[
                ModelOption(
                    repo_id="lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF",
                    label="Meta-Llama-3.1-8B-Instruct-GGUF",
                    has_token=False,
                    variants=[
                        ModelOption(
                            value="Meta-Llama-3.1-8B-Instruct-IQ4_XS.gguf",
                            label="Meta-Llama-3.1-8B-Instruct-IQ4_XS",
                            size="4.45GB",
                        ),
                        ModelOption(
                            value="Meta-Llama-3.1-8B-Instruct-Q3_K_L.gguf",
                            label="Meta-Llama-3.1-8B-Instruct-Q3_K_L",
                            size="4.32GB",
                        ),
                        ModelOption(
                            value="Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf",
                            label="Meta-Llama-3.1-8B-Instruct-Q4_K_M",
                            size="4.92GB",
                        ),
                        ModelOption(
                            value="Meta-Llama-3.1-8B-Instruct-Q5_K_M.gguf",
                            label="Meta-Llama-3.1-8B-Instruct-Q5_K_M",
                            size="5.73GB",
                        ),
                        ModelOption(
                            value="Meta-Llama-3.1-8B-Instruct-Q6_K.gguf",
                            label="Meta-Llama-3.1-8B-Instruct-Q6_K",
                            size="6.60GB",
                        ),
                        ModelOption(
                            value="Meta-Llama-3.1-8B-Instruct-Q8_0.gguf",
                            label="Meta-Llama-3.1-8B-Instruct-Q8_0",
                            size="8.54GB",
                        ),
                    ],
                ),
                ModelOption(
                    repo_id="QuantFactory/NuExtract-GGUF",
                    label="NuExtract-GGUF",
                    has_token=False,
                    variants=[
                        ModelOption(
                            value="NuExtract.Q8_0.gguf",
                            label="NuExtract.Q8_0",
                            size="4.06GB",
                        ),
                    ],
                ),
            ],
        ),
    ]
    return SUPPORTED_MODELS
