import pandas as pd
import sqlite3
import logging
from typing import Tuple, Any, Optional, Dict, Union
from pathlib import Path
import re

from app.services.sources.db.base import DatabaseClient
from app.utils.query_result import QueryResult

logger = logging.getLogger(__name__)


class CSVClient(DatabaseClient):
    def __init__(self, path: Union[str, Path]):
        """
        Initialize CSV client with either a single CSV file or a directory containing CSV files.

        Args:
            path (Union[str, Path]): Path to either a CSV file or directory containing CSV files
        """
        self.path = Path(path)
        self.is_single_file = self.path.is_file()
        self.dataframes: Dict[str, pd.DataFrame] = {}
        self.sqlite_connection = None
        self.table_name_mapping: Dict[str, str] = {}
        self.reverse_table_name_mapping: Dict[str, str] = {}
        self.blacklist = [
            r"\bDROP\s+TABLE\b",
            r"\bDELETE\s+FROM\b",
            r"\bDROP\s+DATABASE\b",
            r"\bTRUNCATE\s+TABLE\b",
            r"\bALTER\s+TABLE\b.*\bDROP\b",
        ]
        self._initialize_sqlite()
        self._load_csv_data()

    def _check_blacklist(self, query: str) -> bool:
        """Check if query contains any blacklisted operations"""
        for pattern in self.blacklist:
            if re.search(pattern, query, re.IGNORECASE):
                return True
        return False

    def _sanitize_table_name(self, original_name: str) -> str:
        """Convert a file name to a valid SQLite table name."""
        # Replace invalid characters with underscores
        sanitized = re.sub(r"[^a-zA-Z0-9_]", "_", original_name)

        # Ensure the name starts with a letter or underscore
        if sanitized[0].isdigit():
            sanitized = f"t_{sanitized}"

        # If the name is a SQLite keyword, prefix it
        sqlite_keywords = {
            "table",
            "index",
            "select",
            "where",
            "from",
            "as",
            "or",
            "and",
            "order",
            "by",
            "group",
        }
        if sanitized.lower() in sqlite_keywords:
            sanitized = f"tbl_{sanitized}"

        return sanitized

    def _initialize_sqlite(self):
        """Initialize in-memory SQLite database"""
        self.sqlite_connection = sqlite3.connect(":memory:")
        self.sqlite_connection.row_factory = sqlite3.Row

    def _load_csv_data(self):
        """Load CSV data based on whether input is a single file or directory"""
        if not self.path.exists():
            raise FileNotFoundError(f"Path not found: {self.path}")

        if self.is_single_file:
            if not self.path.suffix.lower() == ".csv":
                raise ValueError(f"File must be a CSV file: {self.path}")
            self._load_single_csv(self.path)
        else:
            self._load_csv_directory()

    def _load_single_csv(self, file_path: Path):
        """Load a single CSV file"""
        original_name = file_path.stem
        sanitized_name = self._sanitize_table_name(original_name)

        # For single file, also support using "data" as the table name
        default_name = "data"
        self.table_name_mapping[original_name] = sanitized_name
        self.table_name_mapping[default_name] = sanitized_name
        self.reverse_table_name_mapping[sanitized_name] = original_name

        try:
            df = pd.read_csv(file_path)
            self.dataframes[original_name] = df
            df.to_sql(
                sanitized_name, self.sqlite_connection, if_exists="replace", index=False
            )
            logger.info(f"Loaded CSV file: {file_path} as table: {sanitized_name}")
        except Exception as e:
            logger.error(f"Error loading {file_path}: {e}")
            raise

    def _load_csv_directory(self):
        """Load all CSV files from a directory"""
        csv_files = list(self.path.glob("*.csv"))
        if not csv_files:
            raise ValueError(f"No CSV files found in directory: {self.path}")

        for file_path in csv_files:
            original_name = file_path.stem
            sanitized_name = self._sanitize_table_name(original_name)

            self.table_name_mapping[original_name] = sanitized_name
            self.reverse_table_name_mapping[sanitized_name] = original_name

            try:
                df = pd.read_csv(file_path)
                self.dataframes[original_name] = df
                df.to_sql(
                    sanitized_name,
                    self.sqlite_connection,
                    if_exists="replace",
                    index=False,
                )
                logger.info(f"Loaded CSV file: {file_path} as table: {sanitized_name}")
            except Exception as e:
                logger.error(f"Error loading {file_path}: {e}")

    @property
    def db_type(self) -> str:
        return "SQLite"

    def get_tablenames(self) -> str:
        """Get names of all available CSV files (tables)"""
        return ", ".join(self.dataframes.keys())

    def _get_sanitized_table_name(self, original_name: str) -> str:
        """Get the sanitized table name for a given original name"""
        return self.table_name_mapping.get(original_name, original_name)

    def _get_original_table_name(self, sanitized_name: str) -> str:
        """Get the original table name for a given sanitized name"""
        return self.reverse_table_name_mapping.get(sanitized_name, sanitized_name)

    def get_schema(self) -> str:
        """
        Get schema information for all CSV files in SQL format
        Uses SQLite schema information enhanced with pandas statistics
        """
        schemas = []

        for original_name, df in self.dataframes.items():
            sanitized_name = self._get_sanitized_table_name(original_name)
            cursor = self.sqlite_connection.cursor()

            # Get SQLite table info using sanitized name
            cursor.execute(f"PRAGMA table_info({sanitized_name})")
            columns = cursor.fetchall()

            # Build CREATE TABLE statement using original name for display
            create_statement = [f"CREATE TABLE {original_name} ("]
            column_definitions = []

            for col in columns:
                col_name = col["name"]
                col_type = col["type"]

                # Add statistics for the column
                if col_type in ["INTEGER", "REAL"]:
                    stats = df[col_name].describe()
                    column_definitions.append(
                        f"    {col_name} {col_type}  -- min: {stats['min']:.2f}, max: {stats['max']:.2f}, "
                        f"avg: {stats['mean']:.2f}, null: {df[col_name].isnull().sum()}"
                    )
                else:
                    unique_count = df[col_name].nunique()
                    null_count = df[col_name].isnull().sum()
                    column_definitions.append(
                        f"    {col_name} {col_type}  -- unique values: {unique_count}, null: {null_count}"
                    )

            create_statement.extend([",\n".join(column_definitions), ");"])

            if sanitized_name != original_name:
                create_statement.append(
                    f"\n-- Note: This table is stored internally as: {sanitized_name}"
                )

            schemas.append("\n".join(create_statement))
        return "\n\n".join(schemas)

    def execute_query(
        self, query: str, parameters: Optional[Tuple[Any, ...]] = None
    ) -> QueryResult:
        """
        Execute SQL query directly using SQLite, handling table name translation
        """
        if self._check_blacklist(query):
            return QueryResult(
                success=False,
                data=[],
                error_message="Query contains blacklisted commands",
            )

        # Replace original table names with sanitized ones in the query
        modified_query = query
        for original_name, sanitized_name in self.table_name_mapping.items():
            # Use word boundaries to avoid partial replacements
            pattern = r"\b" + re.escape(original_name) + r"\b"
            modified_query = re.sub(pattern, sanitized_name, modified_query)

        cursor = self.sqlite_connection.cursor()
        try:
            if parameters:
                cursor.execute(modified_query, parameters)
            else:
                cursor.execute(modified_query)

            if query.strip().upper().startswith("SELECT"):
                data = cursor.fetchall()
                column_names = [description[0] for description in cursor.description]
                return QueryResult(
                    success=True,
                    data=[tuple(row) for row in data],
                    affected_rows=len(data),
                    column_names=column_names,
                )
            else:
                self.sqlite_connection.commit()
                return QueryResult(success=True, data=[], affected_rows=cursor.rowcount)
        except sqlite3.Error as e:
            return QueryResult(
                success=False,
                data=[],
                error_message=f"SQLite error: {str(e)}\nModified query: {modified_query}",
            )
        finally:
            cursor.close()

    def get_table_summary(self, table_name: str) -> str:
        """
        Get a detailed summary of a specific table, useful for LLM context
        """
        if table_name not in self.dataframes:
            return f"Table '{table_name}' not found"

        df = self.dataframes[table_name]
        summary = []

        summary.append(f"Table: {table_name}")
        summary.append(f"Total Rows: {len(df)}")
        summary.append(f"Total Columns: {len(df.columns)}")
        summary.append("\nColumn Statistics:")

        for column in df.columns:
            col_type = df[column].dtype
            null_count = df[column].isnull().sum()
            unique_count = df[column].nunique()

            summary.append(f"\n{column} ({col_type}):")
            summary.append(f"  - Unique Values: {unique_count}")
            summary.append(f"  - Null Values: {null_count}")

            if pd.api.types.is_numeric_dtype(df[column]):
                stats = df[column].describe()
                summary.append(f"  - Min: {stats['min']:.2f}")
                summary.append(f"  - Max: {stats['max']:.2f}")
                summary.append(f"  - Mean: {stats['mean']:.2f}")
                summary.append(f"  - Std Dev: {stats['std']:.2f}")
            elif pd.api.types.is_string_dtype(df[column]):
                # For text columns, show sample of unique values
                unique_samples = df[column].dropna().unique()[:5]
                summary.append(
                    f"  - Sample Values: {', '.join(str(x) for x in unique_samples)}"
                )

        return "\n".join(summary)

    def get_table_preview(self, table_name: str, n_rows: int = 5) -> str:
        """Get a preview of the table's data"""
        if table_name not in self.dataframes:
            return f"Table '{table_name}' not found"

        sanitized_name = self._get_sanitized_table_name(table_name)
        cursor = self.sqlite_connection.cursor()
        try:
            cursor.execute(f"SELECT * FROM {sanitized_name} LIMIT {n_rows}")
            rows = cursor.fetchall()
            if not rows:
                return f"No data found in table '{table_name}'"

            column_names = [description[0] for description in cursor.description]
            preview_df = pd.DataFrame(rows, columns=column_names)
            return preview_df.to_string()
        except sqlite3.Error as e:
            return f"Error getting preview: {str(e)}"
        finally:
            cursor.close()

    def __del__(self):
        """Cleanup SQLite connection on object destruction"""
        if self.sqlite_connection:
            self.sqlite_connection.close()
