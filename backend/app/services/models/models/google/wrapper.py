from typing import Any, List, Optional, Union, Generator

from ..base import LLMInterface, TaskType, CompletionResponse, EmbeddingResponse


class GoogleAIWrapper(LLMInterface):
    """Wrapper for Google AI models"""

    def __init__(self, model: Any):
        self._model = model
        self._embedding_model = None

    @property
    def model_name(self) -> str:
        return self._model.model_name

    @property
    def model_types(self) -> List[TaskType]:
        return [TaskType.COMPLETION, TaskType.CHAT, TaskType.EMBEDDING]

    def complete(
        self,
        prompt: str,
        max_tokens: Optional[int] = None,
        temperature: float = 0.7,
        top_p: float = 1.0,
        stop: Optional[Union[str, List[str]]] = None,
        stream: bool = False,
    ) -> Union[CompletionResponse, Generator[CompletionResponse, None, None]]:
        generation_config = {
            "temperature": temperature,
            "top_p": top_p,
            "max_output_tokens": max_tokens,
            "stop_sequences": stop
            if isinstance(stop, list)
            else [stop]
            if stop
            else None,
        }
        generation_config = {
            k: v for k, v in generation_config.items() if v is not None
        }

        try:
            if stream:
                response_stream = self._model.generate_content(
                    prompt, generation_config=generation_config, stream=True
                )
                return (
                    CompletionResponse(
                        text=chunk.text,
                        finish_reason="stop" if i == len(response_stream) - 1 else None,
                    )
                    for i, chunk in enumerate(response_stream)
                )
            else:
                response = self._model.generate_content(
                    prompt, generation_config=generation_config
                )
                return CompletionResponse(text=response.text, finish_reason="stop")
        except Exception as e:
            raise RuntimeError(f"Error in Google AI completion: {str(e)}")

    def embed(self, text: str) -> EmbeddingResponse:
        try:
            if self._embedding_model is None:
                import google.generativeai as genai

                self._embedding_model = genai.GenerativeModel("embedding-001")

            result = self._embedding_model.embed_content(text)
            return EmbeddingResponse(
                embedding=result.embedding, model_name="embedding-001"
            )
        except Exception as e:
            raise RuntimeError(f"Error in Google AI embedding: {str(e)}")
