import os
import shutil
import logging
from abc import ABC, abstractmethod
from typing import List, Optional, Dict
from huggingface_hub import (
    hf_hub_download,
    HfApi,
    HfFolder
)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class HuggingFaceAuth:
    def __init__(self, token: Optional[str] = None):
        self.token = token or HfFolder.get_token()
        self.api = HfApi(token=self.token) if self.token else None

    def validate_token(self) -> bool:
        if not self.token:
            logger.warning("No Hugging Face token provided. Some operations may be restricted.")
            return False
        try:
            self.api.whoami()
            logger.info("Hugging Face authentication successful")
            return True
        except Exception as e:
            logger.error(f"Hugging Face authentication failed: {e}")
            return False


class ModelDownloader(ABC):
    @abstractmethod
    def download(self, repo_id: str, save_path: str, force: bool = False, model_name: Optional[str] = None) -> str:
        pass


class HuggingFaceDownloader(ModelDownloader):
    def __init__(self, auth: Optional[HuggingFaceAuth] = None):
        self.auth = auth

    def download(self, repo_id: str, save_path: str, force: bool = False, model_name: Optional[str] = None) -> str:
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


class ModelManager:
    def __init__(self, base_path: str, hf_token: Optional[str] = None):
        self.base_path = base_path
        self.hf_auth = HuggingFaceAuth(hf_token) if hf_token else None
        self.downloaders = {
            "huggingface": HuggingFaceDownloader(self.hf_auth)
        }

    def download_model(self, repo_id: str, source: str = "huggingface", force: bool = False, model_name: Optional[str] = None) -> str:
        if source not in self.downloaders:
            raise ValueError(f"Unsupported source: {source}")

        save_path = os.path.join(self.base_path, source, repo_id)
        os.makedirs(save_path, exist_ok=True)

        if not force and self.model_exists(repo_id, source, model_name):
            logger.info(f"Repo ID {repo_id} {'file ' + model_name if model_name else ''} already exists. Use force=True to re-download.")
            return os.path.join(save_path, model_name) if model_name else save_path

        downloader = self.downloaders[source]
        try:
            logger.info(f"Repo ID {repo_id} {'file ' + model_name if model_name else ''} downloading")
            model_path = downloader.download(repo_id, save_path, force, model_name)
            logger.info(f"Repo ID {repo_id} {'file ' + model_name if model_name else ''} downloaded successfully.")
            return model_path
        except Exception as e:
            logger.error(f"Failed to download model {repo_id}: {e}")
            raise

    def model_exists(self, repo_id: str, source: str = "huggingface", model_name: Optional[str] = None) -> bool:
        model_path = os.path.join(self.base_path, source, repo_id)
        if model_name:
            return os.path.exists(os.path.join(model_path, model_name))
        return os.path.exists(model_path)

    def delete_model(self, repo_id: str, source: str = "huggingface") -> None:
        model_path = os.path.join(self.base_path, source, repo_id)
        if os.path.exists(model_path):
            shutil.rmtree(model_path)
            logger.info(f"Repo ID {repo_id} deleted successfully.")
        else:
            logger.warning(f"Repo ID {repo_id} not found.")

    def list_models(self, source: Optional[str] = None) -> List[str]:
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

    def add_source(self, source_name: str, downloader: ModelDownloader) -> None:
        self.downloaders[source_name] = downloader

    def get_model_path(self, repo_id: str, source: str = "huggingface") -> str:
        model_path = os.path.join(self.base_path, source, repo_id)
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Repo ID {repo_id} from source {source} not found.")
        return model_path

    def get_model_info(self, repo_id: str, source: str = "huggingface") -> Dict[str, any]:
        model_path = self.get_model_path(repo_id, source)
        return {
            "name": repo_id,
            "source": source,
            "path": model_path,
            "size": self.get_model_size(repo_id, source),
            "last_modified": os.path.getmtime(model_path)
        }

    def get_model_size(self, repo_id: str, source: str = "huggingface") -> int:
        model_path = self.get_model_path(repo_id, source)
        return sum(os.path.getsize(os.path.join(dirpath, model_name))
                   for dirpath, _, model_names in os.walk(model_path)
                   for model_name in model_names)

    def rename_model(self, old_name: str, new_name: str, source: str = "huggingface") -> None:
        old_path = self.get_model_path(old_name, source)
        new_path = os.path.join(self.base_path, source, new_name)
        os.rename(old_path, new_path)
        logger.info(f"Repo ID renamed from {old_name} to {new_name}")

    def copy_model(self, repo_id: str, new_name: str, source: str = "huggingface") -> None:
        src_path = self.get_model_path(repo_id, source)
        dst_path = os.path.join(self.base_path, source, new_name)
        shutil.copytree(src_path, dst_path)
        logger.info(f"Repo ID {repo_id} copied to {new_name}")

    def clear_cache(self) -> None:
        for source in os.listdir(self.base_path):
            source_path = os.path.join(self.base_path, source)
            if os.path.isdir(source_path):
                shutil.rmtree(source_path)
        logger.info("All cached models have been cleared.")

    def get_total_size(self) -> int:
        return sum(self.get_model_size(model, source)
                   for source in os.listdir(self.base_path)
                   for model in os.listdir(os.path.join(self.base_path, source)))

    def list_sources(self) -> List[str]:
        return list(self.downloaders.keys())
