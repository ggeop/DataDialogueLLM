from abc import ABC, abstractmethod
from typing import Tuple, Any, Optional

from app.utils.query_result import QueryResult


class DatabaseClient(ABC):
    @property
    @abstractmethod
    def db_type(self) -> str:
        pass

    @abstractmethod
    def get_tablenames(self) -> str:
        pass

    @abstractmethod
    def get_schema(self) -> str:
        pass

    @abstractmethod
    def execute_query(self, sql: str, parameters: Optional[Tuple[Any, ...]] = None) -> QueryResult:
        pass
