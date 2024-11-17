from typing import Any, List, Optional, Union, Generator

from ..base import LLMInterface, TaskType, CompletionResponse, EmbeddingResponse


class LlamaWrapper(LLMInterface):
    """Wrapper for Llama models"""

    def __init__(self, model: Any):
        self._model = model

    @property
    def model_name(self) -> str:
        return "llama-gguf"  # Or extract from model metadata if available

    @property
    def model_types(self) -> List[TaskType]:
        return [TaskType.COMPLETION]  # Add EMBEDDING if model supports it

    def complete(
        self,
        prompt: str,
        max_tokens: Optional[int] = None,
        temperature: float = 0.7,
        top_p: float = 1.0,
        stop: Optional[Union[str, List[str]]] = None,
        stream: bool = False,
    ) -> Union[CompletionResponse, Generator[CompletionResponse, None, None]]:
        try:
            if stream:
                response_stream = self._model.create_completion(
                    prompt,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    top_p=top_p,
                    stop=stop,
                    stream=True,
                )
                return (
                    CompletionResponse(
                        text=chunk["choices"][0]["text"],
                        finish_reason=chunk["choices"][0].get("finish_reason"),
                        prompt_tokens=chunk.get("usage", {}).get("prompt_tokens"),
                        completion_tokens=chunk.get("usage", {}).get(
                            "completion_tokens"
                        ),
                        total_tokens=chunk.get("usage", {}).get("total_tokens"),
                    )
                    for chunk in response_stream
                )
            else:
                response = self._model.create_completion(
                    prompt,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    top_p=top_p,
                    stop=stop,
                    stream=False,
                    echo=False,
                )
                return CompletionResponse(
                    text=response["choices"][0]["text"],
                    finish_reason=response["choices"][0].get("finish_reason"),
                    prompt_tokens=response.get("usage", {}).get("prompt_tokens"),
                    completion_tokens=response.get("usage", {}).get(
                        "completion_tokens"
                    ),
                    total_tokens=response.get("usage", {}).get("total_tokens"),
                )
        except Exception as e:
            raise RuntimeError(f"Error in Llama completion: {str(e)}")

    def embed(self, text: str) -> EmbeddingResponse:
        raise NotImplementedError("Embedding not supported for this model")
