from typing import Any, List, Optional, Union, Generator
from ..base import LLMInterface, TaskType, CompletionResponse, EmbeddingResponse


class OpenAIWrapper(LLMInterface):
    def __init__(self, client: Any, model_name: str):
        self._client = client
        self._model_name = model_name

    @property
    def model_name(self) -> str:
        return self._model_name

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
        try:
            params = {
                "model": self._model_name,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": temperature,
                "top_p": top_p,
                "stream": stream,
            }
            if max_tokens:
                params["max_tokens"] = max_tokens
            if stop:
                params["stop"] = stop if isinstance(stop, list) else [stop]

            if stream:
                response_stream = self._client.chat.completions.create(**params)

                def generate_responses():
                    for chunk in response_stream:
                        if chunk.choices[0].delta.content:
                            yield CompletionResponse(
                                text=chunk.choices[0].delta.content,
                                finish_reason=chunk.choices[0].finish_reason,
                            )

                return generate_responses()
            else:
                response = self._client.chat.completions.create(**params)
                return CompletionResponse(
                    text=response.choices[0].message.content,
                    finish_reason=response.choices[0].finish_reason,
                    prompt_tokens=response.usage.prompt_tokens,
                    completion_tokens=response.usage.completion_tokens,
                    total_tokens=response.usage.total_tokens,
                )
        except Exception as e:
            raise RuntimeError(f"Error in OpenAI completion: {str(e)}")

    def embed(self, text: str) -> EmbeddingResponse:
        try:
            response = self._client.embeddings.create(
                model="text-embedding-3-small", input=text
            )
            return EmbeddingResponse(
                embedding=response.data[0].embedding,
                model_name="text-embedding-3-small",
            )
        except Exception as e:
            raise RuntimeError(f"Error in OpenAI embedding: {str(e)}")
