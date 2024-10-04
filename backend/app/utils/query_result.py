from dataclasses import dataclass
from typing import List, Tuple, Any


@dataclass
class QueryResult:
    success: bool
    data: List[Tuple[Any, ...]]
    error_message: str = ""
    affected_rows: int = 0
    column_names: List[str] = None
