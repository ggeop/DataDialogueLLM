import re
import os
import socket
import logging
from contextlib import contextmanager
from typing import Tuple, Any, Optional

import mysql.connector

from app.services.sources.db.base import DatabaseClient
from app.utils.query_result import QueryResult


logger = logging.getLogger(__name__)


class MySQLClient(DatabaseClient):
    def __init__(self, dbname: str, user: str, password: str, host: str, port: str):
        self.connection_params = {
            "database": dbname,
            "user": user,
            "password": password,
            "host": self._resolve_docker_host(host),
            "port": port,
        }
        self.connection = None
        self.blacklist = [
            r"\bDROP\s+TABLE\b",
            r"\bDELETE\s+FROM\b",
            r"\bDROP\s+DATABASE\b",
            r"\bTRUNCATE\s+TABLE\b",
            r"\bALTER\s+TABLE\b.*\bDROP\b",
        ]

    def _resolve_docker_host(self, host: str) -> str:
        if host == "localhost" or host == "127.0.0.1":
            if os.path.exists("/.dockerenv"):
                try:
                    return socket.gethostbyname("host.docker.internal")
                except socket.gaierror:
                    return self._get_docker_host_ip()
        return host

    def _get_docker_host_ip(self) -> str:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]

    @property
    def db_type(self) -> str:
        return "MySQL"

    @contextmanager
    def get_connection(self):
        if self.connection:
            yield self.connection
        else:
            try:
                conn = mysql.connector.connect(**self.connection_params)
                yield conn
            except mysql.connector.Error as e:
                logger.info(f"Connection error: {e}")
                logger.info(f"Attempted to connect with: {self.connection_params}")
                logger.info(
                    "Please check your MySQL server status and connection details."
                )
                raise
            finally:
                if "conn" in locals() and conn is not None:
                    conn.close()

    def test_connection(self):
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT 1")
                    result = cursor.fetchone()
                    if result == (1,):
                        logger.info("Connection successful!")
                    else:
                        logger.info("Connection test failed.")
        except Exception as e:
            logger.info(f"Connection test failed: {e}")

    def get_tablenames(self) -> str:
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SHOW TABLES")
                tables = cursor.fetchall()
                table_names = [table[0] for table in tables]
                return ", ".join(table_names)

    def get_schema(self) -> str:
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SHOW TABLES")
                tables = cursor.fetchall()

                create_statements = []

                for table in tables:
                    table_name = table[0]

                    # Get CREATE TABLE statement directly from MySQL
                    cursor.execute(f"SHOW CREATE TABLE {table_name}")
                    create_table = cursor.fetchone()

                    if create_table and len(create_table) > 1:
                        create_statements.append(create_table[1])

                return "\n\n".join(create_statements)

    def _format_data_type(
        self,
        col_type: str,
        char_max_length: Optional[int],
        num_precision: Optional[int],
        num_scale: Optional[int],
    ) -> str:
        """Helper method to format data type with proper precision/scale"""
        if col_type == "varchar":
            return f"VARCHAR({char_max_length})" if char_max_length else "VARCHAR"
        elif col_type == "char":
            return f"CHAR({char_max_length})" if char_max_length else "CHAR"
        elif col_type in ["numeric", "decimal"]:
            if num_precision is not None:
                if num_scale is not None:
                    return f"{col_type.upper()}({num_precision},{num_scale})"
                return f"{col_type.upper()}({num_precision})"
        return col_type.upper()

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
            with conn.cursor() as cursor:
                try:
                    if parameters:
                        cursor.execute(sql, parameters)
                    else:
                        cursor.execute(sql)

                    if sql.strip().upper().startswith("SELECT"):
                        data = cursor.fetchall()
                        column_names = [desc[0] for desc in cursor.description]
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
                except mysql.connector.Error as e:
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
