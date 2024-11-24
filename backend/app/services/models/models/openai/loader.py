from typing import Optional
from ..base import LLMInterface, ModelLoader
from .wrapper import OpenAIWrapper
from ...model_file_manager import ModelFileManager
from ...downloader import ModelDownloader


class OpenAILoader(ModelLoader):
    def __init__(self, api_key: str):
        """Initialize OpenAI loader."""
        from openai import OpenAI

        self.client = OpenAI(api_key=api_key)

    def load_model(
        self,
        repo_id: str,
        model_name: str,
        source: str,
        file_manager: ModelFileManager,
        downloader: Optional[ModelDownloader] = None,
        force_download: bool = False,
        **kwargs
    ) -> LLMInterface:
        """Load an OpenAI model."""
        return OpenAIWrapper(self.client, model_name)
