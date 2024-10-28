import re
import socket
import psycopg2
import os
import socket
import logging
from contextlib import contextmanager
from typing import Tuple, Any, Optional

from app.clients.db.base import DatabaseClient
from app.utils.query_result import QueryResult


logger = logging.getLogger(__name__)


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
                logger.info(f"Connection error: {e}")
                logger.info(f"Attempted to connect with: {self.connection_params}")
                logger.info("Please check your PostgreSQL server status and connection details.")
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
                        logger.info("Connection successful!")
                    else:
                        logger.info("Connection test failed.")
        except Exception as e:
            logger.info(f"Connection test failed: {e}")

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

                create_statements = []
                
                for table in tables:
                    table_name = table[0]
                    
                    # Get column information
                    cursor.execute("""
                        SELECT 
                            column_name, 
                            data_type,
                            character_maximum_length,
                            numeric_precision,
                            numeric_scale,
                            is_nullable,
                            column_default,
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
                        ORDER BY ordinal_position
                    """, (table_name,))
                    columns = cursor.fetchall()

                    # Start building CREATE TABLE statement
                    create_statement = [f"CREATE TABLE {table_name} ("]
                    column_definitions = []

                    for col in columns:
                        (col_name, col_type, char_max_length, num_precision, 
                         num_scale, is_nullable, default, is_pk) = col
                        
                        # Format the data type
                        formatted_type = self._format_data_type(
                            col_type, char_max_length, num_precision, num_scale
                        )
                        
                        # Build column definition
                        parts = [f"{col_name} {formatted_type}"]
                        
                        if not is_nullable == 'YES':
                            parts.append("NOT NULL")
                        if default is not None:
                            parts.append(f"DEFAULT {default}")
                        if is_pk:
                            parts.append("PRIMARY KEY")
                            
                        column_definitions.append("    " + " ".join(parts))

                    # Get foreign key constraints
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

                    # Add foreign key constraints
                    for fk in foreign_keys:
                        from_col, to_table, to_col = fk
                        column_definitions.append(
                            f"    FOREIGN KEY ({from_col}) REFERENCES {to_table}({to_col})"
                        )

                    create_statement.extend([",\n".join(column_definitions), ");"])
                    create_statements.append("\n".join(create_statement))

                return "\n\n".join(create_statements)

    def _format_data_type(self, col_type: str, char_max_length: Optional[int],
                          num_precision: Optional[int], num_scale: Optional[int]) -> str:
        """Helper method to format data type with proper precision/scale"""
        if col_type == 'character varying':
            return f"VARCHAR({char_max_length})" if char_max_length else "VARCHAR"
        elif col_type == 'character':
            return f"CHAR({char_max_length})" if char_max_length else "CHAR"
        elif col_type in ['numeric', 'decimal']:
            if num_precision is not None:
                if num_scale is not None:
                    return f"{col_type.upper()}({num_precision},{num_scale})"
                return f"{col_type.upper()}({num_precision})"
        return col_type.upper()

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
