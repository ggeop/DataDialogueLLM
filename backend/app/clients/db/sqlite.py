import re
import sqlite3
from contextlib import contextmanager
from typing import Tuple, Any, Optional

from app.clients.db.base import DatabaseClient
from app.utils.query_result import QueryResult


class SQLiteClient(DatabaseClient):
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.connection = None
        if self.db_path == ":memory:":
            self.connection = sqlite3.connect(":memory:")
        self.blacklist = [
            r"\bDROP\s+TABLE\b",
            r"\bDELETE\s+FROM\b",
            r"\bDROP\s+DATABASE\b",
            r"\bTRUNCATE\s+TABLE\b",
            r"\bALTER\s+TABLE\b.*\bDROP\b",
        ]

    @property
    def db_type(self) -> str:
        return "SQLite"

    @contextmanager
    def get_connection(self):
        if self.connection:
            yield self.connection
        else:
            conn = sqlite3.connect(self.db_path)
            try:
                yield conn
            finally:
                conn.close()

    def get_tablenames(self) -> str:
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Get all table names
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()

            # Create a string with all table names
            table_names = [table[0] for table in tables]
            return ", ".join(table_names)

    def get_schema(self) -> str:
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Get all table names
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()

            schema = []
            for table in tables:
                table_name = table[0]
                schema.append(f"Table: {table_name}")

                # Get column information for each table
                cursor.execute(f"PRAGMA table_info('{table_name}');")
                columns = cursor.fetchall()

                schema.append("Columns:")
                for col in columns:
                    col_name = col[1]
                    col_type = col[2]
                    is_nullable = "NULL" if col[3] == 0 else "NOT NULL"
                    is_pk = "PRIMARY KEY" if col[5] == 1 else ""
                    schema.append(
                        f"  - {col_name} ({col_type}) {is_nullable} {is_pk}".strip()
                    )

                # Get foreign key information
                cursor.execute(f"PRAGMA foreign_key_list('{table_name}');")
                foreign_keys = cursor.fetchall()

                if foreign_keys:
                    schema.append("Foreign Keys:")
                    for fk in foreign_keys:
                        from_col = fk[3]
                        to_table = fk[2]
                        to_col = fk[4]
                        schema.append(f"  - {from_col} -> {to_table}({to_col})")

                schema.append("")  # Empty line between tables

            return "\n".join(schema)

    def execute_query(
        self, sql: str, parameters: Optional[Tuple[Any, ...]] = None
    ) -> QueryResult:
        if self._check_blacklist(sql):
            return QueryResult(
                success=False,
                data=[],
                error_message="Query contains blacklisted commands",
            )

        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                if parameters:
                    cursor.execute(sql, parameters)
                else:
                    cursor.execute(sql)

                if sql.strip().upper().startswith("SELECT"):
                    data = cursor.fetchall()
                    column_names = [
                        description[0] for description in cursor.description
                    ]
                    return QueryResult(
                        success=True,
                        data=data,
                        affected_rows=len(data),
                        column_names=column_names,
                    )
                else:
                    conn.commit()
                    return QueryResult(
                        success=True, data=[], affected_rows=cursor.rowcount
                    )
            except sqlite3.Error as e:
                return QueryResult(success=False, data=[], error_message=str(e))

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None

    def _check_blacklist(self, sql: str) -> bool:
        for pattern in self.blacklist:
            if re.search(pattern, sql, re.IGNORECASE):
                return True
        return False
