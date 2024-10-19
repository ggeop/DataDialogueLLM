from abc import ABC, abstractmethod
from typing import Any
from llama_cpp import Llama


class ModelLoader(ABC):
    @abstractmethod
    def load_model(self, model_path: str, **kwargs) -> Any:
        """
        Abstract method to load a model.

        Args:
            model_path (str): Path to the model file.
            **kwargs: Additional keyword arguments for model loading.

        Returns:
            Any: Loaded model object.
        """
        pass


class GGUFLoader(ModelLoader):
    def load_model(self, model_path: str, **kwargs) -> Llama:
        """
        Load a GGUF model.

        Args:
            model_path (str): Path to the GGUF model file.
            **kwargs: Additional keyword arguments for Llama model.

        Returns:
            Llama: Loaded Llama model object.
        """
        return Llama(model_path=model_path, **kwargs)
