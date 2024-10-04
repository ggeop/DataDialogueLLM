import re
import socket
import psycopg2
import os
import socket
from contextlib import contextmanager
from typing import Tuple, Any, Optional

from app.clients.db.base import DatabaseClient
from app.utils.query_result import QueryResult


class PostgresClient(DatabaseClient):
    def __init__(self, dbname: str, user: str, password: str, host: str, port: str):
        self.connection_params = {
            "dbname": dbname,
            "user": user,
            "password": password,
            "host": self._resolve_docker_host(host),
            "port": port
        }
        self.connection = None
        self.blacklist = [
            r'\bDROP\s+TABLE\b',
            r'\bDELETE\s+FROM\b',
            r'\bDROP\s+DATABASE\b',
            r'\bTRUNCATE\s+TABLE\b',
            r'\bALTER\s+TABLE\b.*\bDROP\b',
        ]

    def _resolve_docker_host(self, host: str) -> str:
        if host == "localhost" or host == "127.0.0.1":
            # Check if we're running inside a Docker container
            if os.path.exists('/.dockerenv'):
                # Try to use host.docker.internal for Docker Desktop
                try:
                    return socket.gethostbyname('host.docker.internal')
                except socket.gaierror:
                    # If host.docker.internal doesn't work, fall back to the host's network interface
                    return self._get_docker_host_ip()
        return host

    def _get_docker_host_ip(self) -> str:
        # This gets the IP address of the host machine from inside the container
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]

    @property
    def db_type(self) -> str:
        return "PostgreSQL"

    @contextmanager
    def get_connection(self):
        if self.connection:
            yield self.connection
        else:
            try:
                conn = psycopg2.connect(**self.connection_params)
                yield conn
            except psycopg2.OperationalError as e:
                print(f"Connection error: {e}")
                print(f"Attempted to connect with: {self.connection_params}")
                print("Please check your PostgreSQL server status and connection details.")
                raise
            finally:
                if 'conn' in locals() and conn is not None:
                    conn.close()

    def test_connection(self):
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT 1")
                    result = cursor.fetchone()
                    if result == (1,):
                        print("Connection successful!")
                    else:
                        print("Connection test failed.")
        except Exception as e:
            print(f"Connection test failed: {e}")

    def get_tablenames(self) -> str:
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT table_name
                    FROM information_schema.tables
                    WHERE table_schema = 'public'
                """)
                tables = cursor.fetchall()
                table_names = [table[0] for table in tables]
                return ", ".join(table_names)

    def get_schema(self) -> str:
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT table_name
                    FROM information_schema.tables
                    WHERE table_schema = 'public'
                """)
                tables = cursor.fetchall()

                schema = []
                for table in tables:
                    table_name = table[0]
                    schema.append(f"Table: {table_name}")

                    # Get column information
                    cursor.execute("""
                        SELECT column_name, data_type, is_nullable, column_default,
                               (SELECT EXISTS (
                                   SELECT 1
                                   FROM information_schema.table_constraints tc
                                   JOIN information_schema.key_column_usage kcu
                                     ON tc.constraint_name = kcu.constraint_name
                                    AND tc.table_schema = kcu.table_schema
                                    AND tc.table_name = kcu.table_name
                                   WHERE tc.constraint_type = 'PRIMARY KEY'
                                     AND tc.table_name = c.table_name
                                     AND kcu.column_name = c.column_name
                               )) as is_primary_key
                        FROM information_schema.columns c
                        WHERE table_name = %s
                    """, (table_name,))
                    columns = cursor.fetchall()

                    schema.append("Columns:")
                    for col in columns:
                        col_name, col_type, is_nullable, default, is_pk = col
                        is_nullable = "NULL" if is_nullable == "YES" else "NOT NULL"
                        is_pk = "PRIMARY KEY" if is_pk else ""
                        default = f"DEFAULT {default}" if default else ""
                        schema.append(f"  - {col_name} ({col_type}) {is_nullable} {default} {is_pk}".strip())

                    # Get foreign key information
                    cursor.execute("""
                        SELECT
                            kcu.column_name,
                            ccu.table_name AS foreign_table_name,
                            ccu.column_name AS foreign_column_name
                        FROM
                            information_schema.table_constraints AS tc
                            JOIN information_schema.key_column_usage AS kcu
                              ON tc.constraint_name = kcu.constraint_name
                              AND tc.table_schema = kcu.table_schema
                            JOIN information_schema.constraint_column_usage AS ccu
                              ON ccu.constraint_name = tc.constraint_name
                              AND ccu.table_schema = tc.table_schema
                        WHERE tc.constraint_type = 'FOREIGN KEY' AND tc.table_name = %s
                    """, (table_name,))
                    foreign_keys = cursor.fetchall()

                    if foreign_keys:
                        schema.append("Foreign Keys:")
                        for fk in foreign_keys:
                            from_col, to_table, to_col = fk
                            schema.append(f"  - {from_col} -> {to_table}({to_col})")

                    schema.append("")  # Empty line between tables

                return "\n".join(schema)

    def execute_query(self, sql: str, parameters: Optional[Tuple[Any, ...]] = None) -> QueryResult:
        if self._check_blacklist(sql):
            return QueryResult(
                success=False,
                data=[],
                error_message="Query contains blacklisted commands"
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
                            column_names=column_names
                        )
                    else:
                        conn.commit()
                        return QueryResult(
                            success=True,
                            data=[],
                            affected_rows=cursor.rowcount
                        )
                except psycopg2.Error as e:
                    return QueryResult(
                        success=False,
                        data=[],
                        error_message=str(e)
                    )

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None

    def _check_blacklist(self, sql: str) -> bool:
        for pattern in self.blacklist:
            if re.search(pattern, sql, re.IGNORECASE):
                return True
        return False
