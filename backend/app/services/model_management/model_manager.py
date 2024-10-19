import os
from typing import Dict, List, Any, Optional
from .model_loader import ModelLoader, GGUFLoader
from .model_downloader import ModelDownloader, HuggingFaceDownloader
from .model_file_manager import ModelFileManager
from .auth import HuggingFaceAuth
from .utils import logger


class ModelManager:
    """
    A class to manage the downloading, loading, and file management of machine learning models.
    """

    def __init__(self, base_path: str, hf_token: Optional[str] = None):
        """
        Initialize ModelManager.

        Args:
            base_path (str): Base path for storing models.
            hf_token (Optional[str]): HuggingFace API token.
        """
        self.file_manager = ModelFileManager(base_path)
        self.hf_auth = HuggingFaceAuth(hf_token) if hf_token else None
        self.downloaders = {
            "huggingface": HuggingFaceDownloader(self.hf_auth)
        }
        self.models: Dict[str, Any] = {}
        self.loaders: Dict[str, ModelLoader] = {
            "gguf": GGUFLoader()
        }

    def load_model(self, repo_id: str, model_name: str, model_type: str, source: str = "huggingface", force_download: bool = False, **kwargs) -> Any:
        """
        Load a model, downloading it first if necessary.

        Args:
            repo_id (str): Repository ID.
            model_name (str): Model name.
            model_type (str): Type of the model.
            source (str): Source of the model (default is "huggingface").
            force_download (bool): Force download even if the model exists locally.
            **kwargs: Additional keyword arguments for model loading.

        Returns:
            Any: Loaded model object.

        Raises:
            ValueError: If the model type is not supported or the source is invalid.
        """
        # Check if the model is already loaded
        model_key = f"{source}/{repo_id}/{model_name}"
        if model_key in self.models and not force_download:
            logger.info(f"Model {model_key} is already loaded. Returning cached model.")
            return self.models[model_key]

        # Check if the model exists locally, if not, download it
        if not self.file_manager.model_exists(repo_id, source, model_name) or force_download:
            logger.info(f"Model {model_key} not found locally or force_download is True. Downloading...")
            try:
                self.download_model(repo_id, source, force_download, model_name)
            except Exception as e:
                logger.error(f"Failed to download model {model_key}: {e}")
                raise

        # Get the path to the model file
        try:
            model_path = self.file_manager.get_model_path(repo_id, model_name, source)
        except FileNotFoundError:
            logger.error(f"Model file for {model_key} not found after download attempt.")
            raise

        # Load the model
        if model_type not in self.loaders:
            raise ValueError(f"Unsupported model type: {model_type}")

        loader = self.loaders[model_type]
        try:
            loaded_model = loader.load_model(model_path, **kwargs)
            self.models[model_key] = loaded_model
            logger.info(f"Model {model_key} loaded successfully.")
            return loaded_model
        except Exception as e:
            logger.error(f"Failed to load model {model_key}: {e}")
            raise

    def download_model(self, repo_id: str, source: str = "huggingface", force: bool = False, model_name: Optional[str] = None) -> str:
        """
        Download a model.

        Args:
            repo_id (str): Repository ID.
            source (str): Source of the model (default is "huggingface").
            force (bool): Force download even if the model exists.
            model_name (Optional[str]): Specific model name to download.

        Returns:
            str: Path to the downloaded model.

        Raises:
            ValueError: If the source is not supported.
            Exception: If download fails.
        """
        if source not in self.downloaders:
            raise ValueError(f"Unsupported source: {source}")

        save_path = os.path.join(self.file_manager.base_path, source, repo_id)
        os.makedirs(save_path, exist_ok=True)

        if not force and self.file_manager.model_exists(repo_id, source, model_name):
            logger.info(f"Model {repo_id} {'file ' + model_name if model_name else ''} already exists. Use force=True to re-download.")
            return os.path.join(save_path, model_name) if model_name else save_path

        downloader = self.downloaders[source]
        try:
            logger.info(f"Downloading model {repo_id} {'file ' + model_name if model_name else ''}")
            model_path = downloader.download(repo_id, save_path, force, model_name)
            logger.info(f"Model {repo_id} {'file ' + model_name if model_name else ''} downloaded successfully.")
            return model_path
        except Exception as e:
            logger.error(f"Failed to download model {repo_id}: {e}")
            raise

    def delete_model(self, repo_id: str, source: str = "huggingface") -> None:
        """
        Delete a model from the cache.

        Args:
            repo_id (str): Repository ID.
            source (str): Source of the model (default is "huggingface").
        """
        self.file_manager.delete_model(repo_id, source)

    def list_models(self, source: Optional[str] = None) -> List[str]:
        """
        List available models.

        Args:
            source (Optional[str]): Source to list models from.

        Returns:
            List[str]: List of available models.
        """
        return self.file_manager.list_models(source)

    def add_source(self, source_name: str, downloader: ModelDownloader) -> None:
        """
        Add a new source for downloading models.

        Args:
            source_name (str): Name of the source.
            downloader (ModelDownloader): Downloader object for the source.
        """
        self.downloaders[source_name] = downloader

    def get_model_info(self, repo_id: str, source: str = "huggingface") -> Dict[str, Any]:
        """
        Get information about a model.

        Args:
            repo_id (str): Repository ID.
            source (str): Source of the model (default is "huggingface").

        Returns:
            Dict[str, Any]: Dictionary containing model information.
        """
        return self.file_manager.get_model_info(repo_id, source)

    def rename_model(self, old_name: str, new_name: str, source: str = "huggingface") -> None:
        """
        Rename a model.

        Args:
            old_name (str): Current name of the model.
            new_name (str): New name for the model.
            source (str): Source of the model (default is "huggingface").
        """
        self.file_manager.rename_model(old_name, new_name, source)

    def copy_model(self, repo_id: str, new_name: str, source: str = "huggingface") -> None:
        """
        Copy a model.

        Args:
            repo_id (str): Repository ID of the model to copy.
            new_name (str): Name for the new copy.
            source (str): Source of the model (default is "huggingface").
        """
        self.file_manager.copy_model(repo_id, new_name, source)

    def get_total_size(self) -> int:
        """
        Get the total size of all cached models.

        Returns:
            int: Total size in bytes.
        """
        return self.file_manager.get_total_size()

    def list_sources(self) -> List[str]:
        """
        List available sources for downloading models.

        Returns:
            List[str]: List of available sources.
        """
        return list(self.downloaders.keys())

    def clear_all_files(self) -> None:
        """
        Clear all model files and reset the loaded models.
        """
        self.file_manager.clear_all_files()
        self.models.clear()
