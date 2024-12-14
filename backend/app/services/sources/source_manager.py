from typing import List
from .config import SourceType


class SourceManager:
    def __init__(self):
        """
        Initialize SourceManager
        """
        pass

    def get_source_names(self) -> List:
        """
        Get a list of supporting sources.

        Returns:
            List[str]: A list of supporting sources.
        """
        return [color.value for color in SourceType]


source_manager_service = SourceManager()
