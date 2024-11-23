from typing import Dict, List, Any, Optional

from .models import ModelLoader
from .downloader import ModelDownloader
from .model_file_manager import ModelFileManager
from .utils import logger


class ModelManager:
    """
    A generic class to manage the loading and file management of machine learning models.
    """

    def __init__(self, base_path: str):
        """
        Initialize ModelManager with support for multiple model sources.

        Args:
            base_path (str): Base path for storing downloadable models
        """
        self.file_manager = ModelFileManager(base_path)
        self.downloaders: Dict[str, ModelDownloader] = {}
        self.models: Dict[str, Any] = {}
        self.loaders: Dict[str, ModelLoader] = {}

    def register_loader(self, format_name: str, loader: ModelLoader) -> None:
        """
        Register a new model loader.

        Args:
            format_name (str): Name/identifier for the model format
            loader (ModelLoader): Loader instance for the format
        """
        self.loaders[format_name] = loader

    def register_downloader(
        self, source_name: str, downloader: ModelDownloader
    ) -> None:
        """
        Register a new model downloader.

        Args:
            source_name (str): Name of the source
            downloader (ModelDownloader): Downloader instance for the source
        """
        self.downloaders[source_name] = downloader

    def load_model(
        self,
        repo_id: str,
        model_name: str,
        model_format: str,
        source: str = "huggingface",
        force_download: bool = False,
        **kwargs,
    ) -> Any:
        """
        Load a model using the appropriate loader.

        Args:
            repo_id (str): Repository ID or model identifier
            model_name (str): Model name
            model_format (str): Model format identifier
            source (str): Source of the model
            force_download (bool): Force download for downloadable models
            **kwargs: Additional keyword arguments for model loading

        Returns:
            Any: Loaded model object

        Raises:
            ValueError: If the model format is not supported or the source is invalid
        """
        if source not in self.loaders:
            raise ValueError(
                f"Unsupported model loader: {source}. Register model loaders: {self.loaders}"
            )

        model_key = f"{source}/{repo_id}/{model_name}"
        logger.info(f"Load model key {model_key}")

        # Return cached model if available
        if model_key in self.models and not force_download:
            logger.info(f"Model {model_key} is already loaded. Returning cached model.")
            return self.models[model_key]
        else:
            logger.info(f"Model {model_key} is not already loaded.")
            loader = self.loaders[source]
            try:
                # Let the loader handle the specifics of loading the model
                # This could involve downloading, API authentication, or loading from disk
                loaded_model = loader.load_model(
                    repo_id=repo_id,
                    model_name=model_name,
                    source=source,
                    file_manager=self.file_manager,
                    downloader=self.downloaders.get(source),
                    force_download=force_download,
                    **kwargs,
                )

                self.models[model_key] = loaded_model
                logger.info(f"Model {model_key} loaded successfully.")
                return loaded_model

            except Exception as e:
                logger.error(f"Failed to load model {model_key}: {e}")
                raise

    def download_model(
        self,
        repo_id: str,
        source: str = "huggingface",
        force: bool = False,
        model_name: Optional[str] = None,
    ) -> str:
        """
        Download a model using the appropriate downloader.

        Args:
            repo_id (str): Repository ID
            source (str): Source of the model
            force (bool): Force download even if model exists
            model_name (Optional[str]): Specific model name to download

        Returns:
            str: Path to the downloaded model

        Raises:
            ValueError: If the source is not supported
        """
        if source not in self.downloaders:
            raise ValueError(f"Unsupported source: {source}")

        save_path = self.file_manager.get_model_path(repo_id, model_name, source)

        if not force and self.file_manager.model_exists(repo_id, source, model_name):
            logger.info(
                f"Model {repo_id} {'file ' + model_name if model_name else ''} already exists. Use force=True to re-download."
            )
            return save_path

        try:
            downloader = self.downloaders[source]
            model_path = downloader.download(repo_id, save_path, force, model_name)
            logger.info(
                f"Model {repo_id} {'file ' + model_name if model_name else ''} downloaded successfully."
            )
            return model_path
        except Exception as e:
            logger.error(f"Failed to download model {repo_id}: {e}")
            raise

    def clear_cache(self) -> None:
        """Clear all cached models."""
        self.models.clear()

    def get_model_info(
        self, repo_id: str, source: str = "huggingface"
    ) -> Dict[str, Any]:
        """Get information about a model."""
        return self.file_manager.get_model_info(repo_id, source)

    def list_models(self, source: Optional[str] = None) -> List[str]:
        """List available models."""
        return self.file_manager.list_models(source)

    def get_total_size(self) -> int:
        """Get total size of all cached models."""
        return self.file_manager.get_total_size()

    def clear_all_files(self) -> None:
        """Clear all model files and reset cache."""
        self.file_manager.clear_all_files()
        self.clear_cache()
        