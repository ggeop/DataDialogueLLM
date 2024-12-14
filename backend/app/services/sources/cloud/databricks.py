import re
import logging
from contextlib import contextmanager
from typing import Tuple, Any, Optional
from databricks import sql
from databricks.sql.client import Connection

from app.services.sources.db.base import DatabaseClient
from app.utils.query_result import QueryResult


logger = logging.getLogger(__name__)


class DatabricksClient(DatabaseClient):
    def __init__(
        self,
        server_hostname: str,
        http_path: str,
        access_token: str,
        catalog: str = "hive_metastore",
        schema: str = "default",
    ):
        self.connection_params = {
            "server_hostname": server_hostname,
            "http_path": http_path,
            "access_token": access_token,
            "catalog": catalog,
            "schema": schema,
        }
        self.connection = None
        self.blacklist = [
            r"\bDROP\s+TABLE\b",
            r"\bDELETE\s+FROM\b",
            r"\bDROP\s+DATABASE\b",
            r"\bTRUNCATE\s+TABLE\b",
            r"\bALTER\s+TABLE\b.*\bDROP\b",
            r"\bVACUUM\b",  # Specific to Delta Lake
            r"\bOPTIMIZE\b",  # Specific to Delta Lake
        ]

    @property
    def db_type(self) -> str:
        return "Databricks Delta Lake"

    @contextmanager
    def get_connection(self) -> Connection:
        if self.connection:
            yield self.connection
        else:
            try:
                conn = sql.connect(
                    server_hostname=self.connection_params["server_hostname"],
                    http_path=self.connection_params["http_path"],
                    access_token=self.connection_params["access_token"],
                    catalog=self.connection_params["catalog"],
                    schema=self.connection_params["schema"],
                )
                yield conn
            except Exception as e:
                logger.error(f"Connection error: {e}")
                logger.error(f"Attempted to connect with: {self.connection_params}")
                logger.error("Please check your Databricks connection details.")
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
            logger.error(f"Connection test failed: {e}")

    def get_tablenames(self) -> str:
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    f"""
                    SHOW TABLES 
                    IN {self.connection_params['catalog']}.{self.connection_params['schema']}
                    """
                )
                tables = cursor.fetchall()
                table_names = [
                    table[1] for table in tables
                ]  # table[1] contains the table name
                return ", ".join(table_names)

    def get_schema(self) -> str:
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                # Get list of tables
                cursor.execute(
                    f"""
                    SHOW TABLES 
                    IN {self.connection_params['catalog']}.{self.connection_params['schema']}
                    """
                )
                tables = cursor.fetchall()

                create_statements = []
                for table in tables:
                    table_name = table[1]  # table[1] contains the table name

                    # Get table description
                    cursor.execute(f"DESCRIBE DETAIL {table_name}")
                    table_detail = cursor.fetchone()

                    # Get column information
                    cursor.execute(f"DESCRIBE {table_name}")
                    columns = cursor.fetchall()

                    # Build CREATE TABLE statement
                    create_statement = [f"CREATE TABLE {table_name} ("]
                    column_definitions = []

                    for col in columns:
                        if (
                            col[0] != "# Detailed Table Information"
                        ):  # Skip metadata section
                            col_name = col[0]
                            col_type = col[1]
                            comment = col[2] if len(col) > 2 and col[2] else ""

                            definition = f"    {col_name} {col_type}"
                            if comment:
                                definition += f" COMMENT '{comment}'"
                            column_definitions.append(definition)

                    create_statement.extend([",\n".join(column_definitions)])

                    # Add Delta-specific properties if available
                    if table_detail:
                        properties = []
                        if "partitionColumns" in str(table_detail):
                            partition_cols = table_detail[
                                4
                            ]  # Adjust index based on actual response
                            if partition_cols:
                                properties.append(
                                    f"    PARTITIONED BY ({', '.join(partition_cols)})"
                                )

                        # Add any cluster by columns if present
                        if "clusteringColumns" in str(table_detail):
                            cluster_cols = table_detail[
                                5
                            ]  # Adjust index based on actual response
                            if cluster_cols:
                                properties.append(
                                    f"    CLUSTERED BY ({', '.join(cluster_cols)})"
                                )

                        if properties:
                            create_statement.append("\n".join(properties))

                    create_statement.append(") USING DELTA")
                    create_statements.append("\n".join(create_statement))

                return "\n\n".join(create_statements)

    def execute_query(
        self, sql_query: str, parameters: Optional[Tuple[Any, ...]] = None
    ) -> QueryResult:
        if self._check_blacklist(sql_query):
            return QueryResult(
                success=False,
                data=[],
                error_message="Query contains blacklisted commands",
            )

        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                try:
                    if parameters:
                        cursor.execute(sql_query, parameters)
                    else:
                        cursor.execute(sql_query)

                    if sql_query.strip().upper().startswith("SELECT"):
                        data = cursor.fetchall()
                        column_names = [desc[0] for desc in cursor.description]
                        return QueryResult(
                            success=True,
                            data=data,
                            affected_rows=len(data),
                            column_names=column_names,
                        )
                    else:
                        # For non-SELECT queries
                        # Note: Databricks SQL connector might not provide rowcount
                        return QueryResult(
                            success=True,
                            data=[],
                            affected_rows=0,  # Actual count might not be available
                        )
                except Exception as e:
                    return QueryResult(success=False, data=[], error_message=str(e))

    def _check_blacklist(self, sql_query: str) -> bool:
        for pattern in self.blacklist:
            if re.search(pattern, sql_query, re.IGNORECASE):
                return True
        return False

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None

    # Delta Lake specific methods
    def get_table_history(self, table_name: str) -> QueryResult:
        """Get the history of changes for a Delta table"""
        query = f"DESCRIBE HISTORY {table_name}"
        return self.execute_query(query)

    def get_table_detail(self, table_name: str) -> QueryResult:
        """Get detailed information about a Delta table"""
        query = f"DESCRIBE DETAIL {table_name}"
        return self.execute_query(query)

    def get_version_at_timestamp(self, table_name: str, timestamp: str) -> QueryResult:
        """Query a Delta table at a specific timestamp"""
        query = f"SELECT * FROM {table_name} TIMESTAMP AS OF '{timestamp}'"
        return self.execute_query(query)

    def get_version(self, table_name: str, version: int) -> QueryResult:
        """Query a Delta table at a specific version"""
        query = f"SELECT * FROM {table_name} VERSION AS OF {version}"
        return self.execute_query(query)
