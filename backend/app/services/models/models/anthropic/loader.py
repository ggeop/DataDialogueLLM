from typing import Optional

from ..base import LLMInterface, ModelLoader
from .wrapper import AnthropicWrapper

from ...model_file_manager import ModelFileManager
from ...downloader import ModelDownloader


class AnthropicLoader(ModelLoader):
    """Loader for Anthropic Claude models."""

    def __init__(self, api_key: str):
        """
        Initialize Claude loader.

        Args:
            api_key (str): Anthropic API key
        """
        from anthropic import Anthropic

        self.api_key = api_key
        self.client = Anthropic(api_key=api_key)

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
        """Load a Claude model."""
        # Claude models are API-based, so we ignore file_manager and downloader
        return AnthropicWrapper(self.client, model_name)
