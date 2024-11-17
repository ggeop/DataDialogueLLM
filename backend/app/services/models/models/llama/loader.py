from typing import Optional, Union, Generator, List, Any

from llama_cpp import Llama

from ..base import LLMInterface, ModelLoader
from .wrapper import LlamaWrapper

from ...model_file_manager import ModelFileManager
from ...downloader import ModelDownloader
from ...utils import logger


class LlamaGGUFLoader(ModelLoader):
    """Loader for GGUF format Llama models."""

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
        """Load a GGUF model."""

        # Download if needed
        if downloader and (
            force_download or not file_manager.model_exists(repo_id, source, model_name)
        ):
            save_path = file_manager.get_model_path(repo_id, model_name, source)
            logger.info(f"Model {model_name} downloading in {save_path}")
            model_path = downloader.download(
                repo_id, save_path, force_download, model_name
            )
        else:
            model_path = file_manager.get_model_path(repo_id, model_name, source)

        # Set default context size if not provided
        kwargs.setdefault("n_ctx", 3000)
        kwargs.setdefault("verbose", False)

        model = Llama(model_path=model_path, **kwargs)
        return LlamaWrapper(model)
