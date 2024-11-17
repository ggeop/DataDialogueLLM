from typing import Optional
from huggingface_hub import HfApi, HfFolder
from .utils import logger


class HuggingFaceAuth:
    def __init__(self, token: Optional[str] = None):
        """
        Initialize HuggingFaceAuth.

        Args:
            token (Optional[str]): HuggingFace API token.
        """
        self.token = token or HfFolder.get_token()
        self.api = HfApi(token=self.token) if self.token else None

    def validate_token(self) -> bool:
        """
        Validate the HuggingFace API token.

        Returns:
            bool: True if token is valid, False otherwise.
        """
        if not self.token:
            logger.warning("No Hugging Face token provided. Some operations may be restricted.")
            return False
        try:
            self.api.whoami()
            logger.info("Hugging Face authentication successful")
            return True
        except Exception as e:
            logger.error(f"Hugging Face authentication failed: {e}")
            return False
