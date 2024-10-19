from abc import ABC, abstractmethod
from typing import Optional
from huggingface_hub import hf_hub_download

from .auth import HuggingFaceAuth
from .utils import logger


class ModelDownloader(ABC):
    @abstractmethod
    def download(self, repo_id: str, save_path: str, force: bool = False, model_name: Optional[str] = None) -> str:
        """
        Abstract method to download a model.

        Args:
            repo_id (str): Repository ID.
            save_path (str): Path to save the downloaded model.
            force (bool): Force download even if the model exists.
            model_name (Optional[str]): Specific model name to download.

        Returns:
            str: Path to the downloaded model.
        """
        pass


class HuggingFaceDownloader(ModelDownloader):
    def __init__(self, auth: Optional[HuggingFaceAuth] = None):
        """
        Initialize HuggingFaceDownloader.

        Args:
            auth (Optional[HuggingFaceAuth]): HuggingFaceAuth object.
        """
        self.auth = auth

    def download(self, repo_id: str, save_path: str, force: bool = False, model_name: Optional[str] = None) -> str:
        """
        Download a model from HuggingFace.

        Args:
            repo_id (str): Repository ID.
            save_path (str): Path to save the downloaded model.
            force (bool): Force download even if the model exists.
            model_name (Optional[str]): Specific model name to download.

        Returns:
            str: Path to the downloaded model.

        Raises:
            Exception: If download fails.
        """
        token = self.auth.token if self.auth else None
        try:
            return hf_hub_download(
                repo_id=repo_id,
                model_name=model_name,
                local_dir=save_path,
                force_download=force,
                token=token
            )
        except Exception as e:
            if token is None:
                logger.warning(f"Download failed. This might be due to missing authentication. Error: {e}")
            else:
                logger.error(f"Download failed. Error: {e}")
            raise
