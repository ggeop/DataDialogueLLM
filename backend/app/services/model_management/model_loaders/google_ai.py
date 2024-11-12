from typing import Any, Dict, Optional, Union
import google.generativeai as genai

from .base import ModelLoader


class GoogleAIModelWrapper:
    """Wrapper for Google AI models to provide Llama-compatible interface."""
    def __init__(self, model: genai.GenerativeModel, **kwargs):
        """
        Initialize the wrapper.

        Args:
            model (genai.GenerativeModel): The underlying Google AI model
        """
        self.model = model
        self.metadata = {"general.name": model.model_name}

    def __call__(self,
                 prompt: str,
                 max_tokens: Optional[int] = None,
                 temperature: float = 0.8,
                 top_p: float = 0.95,
                 stop: Optional[Union[str, list]] = None,
                 stream: bool = False,
                 **kwargs):
        return self.create_completion(
            prompt,
            max_tokens,
            temperature,
            top_p,
            stop,
            stream,
            **kwargs
        )

    def create_completion(
        self,
        prompt: str,
        max_tokens: Optional[int] = None,
        temperature: float = 0.8,
        top_p: float = 0.95,
        stop: Optional[Union[str, list]] = None,
        stream: bool = False,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Create a completion using the Google AI model with a Llama-compatible interface.

        Args:
            prompt (str): The input text prompt
            max_tokens (Optional[int]): Maximum number of tokens to generate
            temperature (float): Sampling temperature (0.0 to 1.0)
            top_p (float): Nucleus sampling parameter
            stop (Optional[Union[str, list]]): Stop sequences
            stream (bool): Whether to stream the response
            **kwargs: Additional parameters

        Returns:
            Dict[str, Any]: Response in Llama-compatible format
        """
        generation_config = {
            'temperature': temperature,
            'top_p': top_p,
            'max_output_tokens': max_tokens,
            'stop_sequences': stop if isinstance(stop, list) else [stop] if stop else None
        }

        # Remove None values
        generation_config = {k: v for k, v in generation_config.items() if v is not None}

        try:
            if stream:
                response = self.model.generate_content(
                    prompt,
                    generation_config=generation_config,
                    stream=True
                )
                # Return a generator that yields in Llama format
                return {
                    'choices': [{
                        'text': chunk.text for chunk in response
                    }]
                }
            else:
                response = self.model.generate_content(
                    prompt,
                    generation_config=generation_config
                )

                return {
                    'choices': [{
                        'text': response.text,
                        'finish_reason': 'stop'
                    }],
                    'usage': {
                        'prompt_tokens': None,  # Google AI doesn't provide token counts
                        'completion_tokens': None,
                        'total_tokens': None
                    }
                }
        except Exception as e:
            raise RuntimeError(f"Error in Google AI model completion: {str(e)}")

    def embed(self, text: str) -> Dict[str, Any]:
        """
        Create embeddings using the Google AI model.

        Args:
            text (str): Input text to embed

        Returns:
            Dict[str, Any]: Embeddings in Llama-compatible format

        Raises:
            NotImplementedError: If the model doesn't support embeddings
        """
        try:
            # Note: You'll need to use a specific embedding model
            embedding_model = genai.GenerativeModel('embedding-001')
            result = embedding_model.embed_content(text)

            return {
                'data': [{
                    'embedding': result.embedding,
                    'index': 0
                }],
                'model': 'embedding-001'
            }
        except Exception as e:
            raise RuntimeError(f"Error in Google AI model embedding: {str(e)}")


class GoogleAILoader(ModelLoader):
    """Loader for Google's Generative AI models."""

    def __init__(self, api_key: str):
        """
        Initialize the Google AI loader.

        Args:
            api_key (str): Google API key for authentication
        """
        self.api_key = api_key
        genai.configure(api_key=api_key)

    def load_model(self, model_name: str, **kwargs) -> GoogleAIModelWrapper:
        """
        Load a Google AI model and wrap it with Llama-compatible interface.

        Args:
            model_name (str): Name of the Google AI model (e.g., 'gemini-1.5-pro')
            **kwargs: Additional configuration parameters for the model

        Returns:
            GoogleAIModelWrapper: Wrapped Google AI model with Llama-compatible interface
        """
        model = genai.GenerativeModel(model_name, **kwargs)
        return GoogleAIModelWrapper(model)
