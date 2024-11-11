from llama_cpp import Llama

from .base import ModelLoader


class LLAMAGGUFLoader(ModelLoader):
    def load_model(self, model_path: str, **kwargs) -> Llama:
        """
        Load a GGUF model.

        Args:
            model_path (str): Path to the GGUF model file.
            **kwargs: Additional keyword arguments for Llama model.

        Returns:
            Llama: Loaded Llama model object.
        """
        return Llama(model_path=model_path,  n_ctx=3000, verbose=False, **kwargs)
