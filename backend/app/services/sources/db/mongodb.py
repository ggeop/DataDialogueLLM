import pymongo

from typing import Tuple, Any, Optional
from app.services.sources.db.base import DatabaseClient
from app.utils.query_result import QueryResult


class MongoDBClient(DatabaseClient):
    def __init__(self, database: str, host: str = "localhost", port: int = 27017):
        self.client = pymongo.MongoClient(host, port)
        self.db = self.client[database]

    @property
    def db_type(self) -> str:
        return "MongoDB"

    def get_tablenames(self) -> str:
        return ", ".join(self.db.list_collection_names())

    def get_schema(self) -> str:
        # MongoDB is schema-less, but we can provide a sample document from each collection
        schemas = []
        for collection_name in self.db.list_collection_names():
            collection = self.db[collection_name]
            sample_doc = collection.find_one()
            if sample_doc:
                schemas.append(
                    f"Collection: {collection_name}\nSample Document Schema:\n{self._format_document_schema(sample_doc)}"
                )
        return "\n\n".join(schemas)

    def _format_document_schema(self, doc: dict, indent: int = 0) -> str:
        schema = []
        for key, value in doc.items():
            if isinstance(value, dict):
                schema.append(f"{'  ' * indent}{key}: {{")
                schema.append(self._format_document_schema(value, indent + 1))
                schema.append(f"{'  ' * indent}}}")
            else:
                schema.append(f"{'  ' * indent}{key}: {type(value).__name__}")
        return "\n".join(schema)

    def execute_query(
        self, query: str, parameters: Optional[Tuple[Any, ...]] = None
    ) -> QueryResult:
        try:
            # For MongoDB, we'll accept a simple query language
            # Format: "collection_name:operation:query"
            collection_name, operation, query_str = query.split(":", 2)
            collection = self.db[collection_name]

            # Parse query string to dict (basic implementation)
            query_dict = eval(query_str) if query_str else {}

            if operation == "find":
                results = list(collection.find(query_dict))
                return QueryResult(
                    success=True,
                    data=results,
                    affected_rows=len(results),
                    column_names=list(results[0].keys()) if results else [],
                )
            elif operation == "insert":
                result = collection.insert_one(query_dict)
                return QueryResult(
                    success=True, data=[str(result.inserted_id)], affected_rows=1
                )
            elif operation == "update":
                result = collection.update_many(
                    query_dict.get("filter", {}), query_dict.get("update", {})
                )
                return QueryResult(
                    success=True, data=[], affected_rows=result.modified_count
                )
            elif operation == "delete":
                result = collection.delete_many(query_dict)
                return QueryResult(
                    success=True, data=[], affected_rows=result.deleted_count
                )
            else:
                return QueryResult(
                    success=False,
                    data=[],
                    error_message=f"Unsupported operation: {operation}",
                )
        except Exception as e:
            return QueryResult(success=False, data=[], error_message=str(e))
