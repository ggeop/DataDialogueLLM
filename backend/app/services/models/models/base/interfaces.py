from abc import ABC, abstractmethod
from typing import Optional, Union, Generator, List
from .types import CompletionResponse, EmbeddingResponse
from .enums import TaskType


from ...model_file_manager import ModelFileManager
from ...downloader import ModelDownloader


class LLMInterface(ABC):
    """Base interface for Language Models"""

    @property
    @abstractmethod
    def model_name(self) -> str:
        """Get the name of the model"""
        pass

    @property
    @abstractmethod
    def model_types(self) -> List[TaskType]:
        """Get the types of tasks this model supports"""
        pass

    @abstractmethod
    def complete(
        self,
        prompt: str,
        max_tokens: Optional[int] = None,
        temperature: float = 0.7,
        top_p: float = 1.0,
        stop: Optional[Union[str, List[str]]] = None,
        stream: bool = False,
    ) -> Union[CompletionResponse, Generator[CompletionResponse, None, None]]:
        """
        Generate completion for the given prompt.

        Args:
            prompt: Input text
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature (0.0 to 1.0)
            top_p: Nucleus sampling parameter
            stop: Stop sequences
            stream: Whether to stream the response

        Returns:
            CompletionResponse or Generator of CompletionResponse for streaming
        """
        pass

    @abstractmethod
    def embed(self, text: str) -> EmbeddingResponse:
        """
        Generate embeddings for the given text.

        Args:
            text: Input text to embed

        Returns:
            EmbeddingResponse containing the embedding vector
        """
        pass


class ModelLoader(ABC):
    @abstractmethod
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
        """
        Load a model with the specific implementation.

        Args:
            repo_id (str): Repository ID or model identifier
            model_name (str): Model name
            source (str): Source of the model
            file_manager (ModelFileManager): File manager instance
            downloader (Optional[ModelDownloader]): Downloader for the source
            force_download (bool): Force download if applicable
            **kwargs: Additional arguments for model loading

        Returns:
            LLMInterface: Loaded model interface
        """
        pass
