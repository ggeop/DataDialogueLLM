# How to add a new model provider

*NOTE: Adding new provider needs few changes in different places. In the future providers configuration can be centralized or even provided from external API*

1. Add a new model `loader.py` and `wrapper.py` under the `backend/app/services/models/models`

    * Create a folder with the provider name e.g `openai`
    * Implement the loader and the wrapper based on the interfaces `ModelLoader` and `LLMInterface`
        ```python
        class NewProviderLoader(ModelLoader):
            def __init__(self, api_key: str):
                self.client = OpenAI(api_key=api_key)

            def load_model(...):

                return NewProviderWrapper(...)

        class NewProviderWrapper(LLMInterface):
            ...

            def complete(...):
                ...

            def embed(...):
                ...
        ```
2. Add the new model provider enum in `ModelSource` under the `backend/app/services/models/models/config.py`

```python
class ModelSource(str, Enum):
    GOOGLE = "google"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    HUGGINGFACE = "huggingface"
    ...

```

3. Utilize the model in the agent_manager service under the `backend/app/services/agents/agent_manager.py`
4. Add the provider logo under the `frontend/static/images/logos`
5. Add the new provider under the supported models API under the `backend/app/api/v1/endpoints/models.py`
