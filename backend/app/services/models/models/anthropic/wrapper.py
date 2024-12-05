from typing import Any, List, Optional, Union, Generator

from ..base import LLMInterface, TaskType, CompletionResponse, EmbeddingResponse


class AnthropicWrapper(LLMInterface):
    """Wrapper for Claude models"""

    def __init__(self, client: Any, model_name: str):
        self._client = client
        self._model_name = model_name

    @property
    def model_name(self) -> str:
        return self._model_name

    @property
    def model_types(self) -> List[TaskType]:
        return [
            TaskType.COMPLETION,
            TaskType.CHAT,
        ]  # Claude doesn't support embeddings natively

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
            message_params = {
                "model": self._model_name,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": temperature,
                "top_p": top_p,
                "stream": stream,
            }

            if max_tokens:
                message_params["max_tokens"] = max_tokens

            if stop:
                message_params["stop_sequences"] = (
                    stop if isinstance(stop, list) else [stop]
                )

            if stream:
                response_stream = self._client.messages.create(**message_params)
                return (
                    CompletionResponse(
                        text=chunk.delta.text if chunk.delta.text else "",
                        finish_reason=(
                            chunk.delta.stop_reason
                            if hasattr(chunk.delta, "stop_reason")
                            else None
                        ),
                    )
                    for chunk in response_stream
                )
            else:
                response = self._client.messages.create(**message_params)
                return CompletionResponse(
                    text=response.content[0].text,
                    finish_reason=(
                        response.stop_reason
                        if hasattr(response, "stop_reason")
                        else "stop"
                    ),
                )
        except Exception as e:
            raise RuntimeError(f"Error in Claude completion: {str(e)}")

    def embed(self, text: str) -> EmbeddingResponse:
        raise NotImplementedError("Claude does not support embeddings natively")
