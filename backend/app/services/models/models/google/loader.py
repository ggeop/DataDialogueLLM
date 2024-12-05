from typing import Optional

from ..base import LLMInterface, ModelLoader
from .wrapper import GoogleAIWrapper


from ...model_file_manager import ModelFileManager
from ...downloader import ModelDownloader


class GoogleAILoader(ModelLoader):
    """Loader for Google AI models."""

    def __init__(self, api_key: str):
        """
        Initialize Google AI loader.

        Args:
            api_key (str): Google AI API key
        """
        import google.generativeai as genai

        self.api_key = api_key
        genai.configure(api_key=api_key)

    def load_model(
        self,
        repo_id: str,
        model_name: str,
        source: str,
        file_manager: ModelFileManager,
        downloader: Optional[ModelDownloader] = None,
        force_download: bool = False,
        **kwargs,
    ) -> LLMInterface:
        """Load a Google AI model."""
        import google.generativeai as genai
        from .wrapper import GoogleAIWrapper

        # Google AI models are API-based, so we ignore file_manager and downloader
        model = genai.GenerativeModel(model_name, **kwargs)
        return GoogleAIWrapper(model)
