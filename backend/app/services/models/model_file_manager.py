import os
import shutil
from typing import Optional, List, Dict, Any

from .utils import logger


class ModelFileManager:
    """
    A class to manage model files on the filesystem.
    """

    def __init__(self, base_path: str):
        """
        Initialize ModelFileManager.

        Args:
            base_path (str): Base path for storing model files.
        """
        self.base_path = base_path

    def get_model_path(self, repo_id: str, model_name: str, source: str = "huggingface") -> str:
        """
        Get the path to a model file.

        Args:
            repo_id (str): Repository ID.
            model_name (Optional[str]): Model name.
            source (str): Source of the model (default is "huggingface").

        Returns:
            str: Path to the model file.
        """
        return os.path.join(self.base_path, source, repo_id, model_name)

    def model_exists(self, repo_id: str, model_name: str, source: str = "huggingface") -> bool:
        """
        Check if a model file exists.

        Args:
            repo_id (str): Repository ID.
            source (str): Source of the model (default is "huggingface").
            model_name (Optional[str]): Specific model name.

        Returns:
            bool: True if the model file exists, False otherwise.
        """
        model_path = self.get_model_path(source, repo_id, model_name)
        return os.path.exists(model_path)

    def delete_model(self, repo_id: str, model_name: str, source: str = "huggingface") -> None:
        """
        Delete a model file.

        Args:
            repo_id (str): Repository ID.
            source (str): Source of the model (default is "huggingface").
        """
        model_path = self.get_model_path(source, repo_id, model_name)
        if os.path.exists(model_path):
            shutil.rmtree(model_path)
            logger.info(f"Model files for Repo ID {repo_id} deleted successfully.")
        else:
            logger.warning(f"Model files for Repo ID {repo_id} not found.")

    def list_models(self, source: Optional[str] = None) -> List[str]:
        """
        List available model files.

        Args:
            source (Optional[str]): Source to list models from.

        Returns:
            List[str]: List of available model files.
        """
        models = []
        if source:
            source_path = os.path.join(self.base_path, source)
            if os.path.exists(source_path):
                models = os.listdir(source_path)
        else:
            for src in os.listdir(self.base_path):
                src_path = os.path.join(self.base_path, src)
                if os.path.isdir(src_path):
                    models.extend([f"{src}/{model}" for model in os.listdir(src_path)])
        return models

    def get_model_info(self, repo_id: str, model_name: str, source: str = "huggingface") -> Dict[str, Any]:
        """
        Get information about a model file.

        Args:
            repo_id (str): Repository ID.
            source (str): Source of the model (default is "huggingface").

        Returns:
            Dict[str, Any]: Dictionary containing model file information.
        """
        model_path = self.get_model_path(source, repo_id, model_name)
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model files for Repo ID {repo_id} from source {source} not found.")

        return {
            "name": repo_id,
            "source": source,
            "path": model_path,
            "size": self.get_model_size(repo_id, source),
            "last_modified": os.path.getmtime(model_path)
        }

    def get_model_size(self, repo_id: str, model_name: str, source: str = "huggingface") -> int:
        """
        Get the size of a model's files.

        Args:
            repo_id (str): Repository ID.
            source (str): Source of the model (default is "huggingface").

        Returns:
            int: Size of the model files in bytes.
        """
        model_path = self.get_model_path(source, repo_id, model_name)
        return sum(os.path.getsize(os.path.join(dirpath, filename))
                   for dirpath, _, filenames in os.walk(model_path)
                   for filename in filenames)

    def get_total_size(self) -> int:
        """
        Get the total size of all model files.

        Returns:
            int: Total size in bytes.
        """
        return sum(self.get_model_size(model, source)
                   for source in os.listdir(self.base_path)
                   for model in os.listdir(os.path.join(self.base_path, source)))

    def clear_all_files(self) -> None:
        """
        Clear all model files.
        """
        for source in os.listdir(self.base_path):
            source_path = os.path.join(self.base_path, source)
            if os.path.isdir(source_path):
                shutil.rmtree(source_path)
        logger.info("All model files have been cleared.")
