from abc import ABC, abstractmethod
from typing import Any


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
