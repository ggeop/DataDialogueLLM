import logging
import re
from typing import Any, Tuple, Optional, Callable
from functools import wraps

from app.utils.query_result import QueryResult

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants for query templates
SQL_GENERATION_TEMPLATE = """Given the following {db_type} database schema:

{schema}

Generate a SQL query to answer the following question:
{question}

Important: 
1. Return ONLY the SQL query, without any markdown formatting, backticks, or explanations.
2. The query should be compatible with {db_type}.
3. Do not use LIMIT unless specifically asked for a limited number of results.
4. Ensure the query retrieves all relevant information to answer the question completely.

SQL query:"""

SQL_CORRECTION_TEMPLATE = """The SQL query you generated resulted in an error: {error}
Please generate a corrected SQL query to answer the following question:
{question}

Important: Return ONLY the corrected SQL query, without any markdown formatting, backticks, or explanations.

Corrected SQL query:"""


def retry_decorator(max_retries: int):
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_retries + 1):
                if attempt > 1:
                    logger.info(f"Attempt {attempt}/{max_retries}")
                result = func(*args, attempt=attempt, **kwargs)
                if result.success:
                    return result
                if attempt < max_retries:
                    logger.warning(f"Attempt {attempt} failed. Retrying...")
            logger.error(f"All {max_retries} attempts failed.")
            return result
        return wrapper
    return decorator


class TextToSQLAgent:
    def __init__(self, language_model: Any,
                 database: Any, max_retries: int = 3,
                 max_tokens: int = 100,
                 initial_temperature: float = 0.3,
                 temperature_increase: float = 0.1):
        self._model = language_model
        self._database = database
        self._max_retries = max_retries
        self._max_tokens = max_tokens
        self._initial_temperature = initial_temperature
        self._temperature_increase = temperature_increase

    def generate(self, question: str) -> Tuple[str, Optional[list], Optional[str]]:
        """
        Generate SQL from a question, execute it, and return the result.
        """
        logger.info("Received question: %s", question)
        sql_result = self._generate_sql_with_retry(question)
        if not sql_result.success:
            return "", None, "Failed to generate SQL query"
        
        sql = sql_result.data[0]  # Extract the SQL string from the QueryResult
        cleaned_sql = self._clean_sql_query(sql)
        logger.info("Cleaned SQL: %s", cleaned_sql)
        
        result = self._execute_query_with_retry(cleaned_sql)
        if result.success:
            return cleaned_sql, result.data, None
        return cleaned_sql, None, result.error_message

    @retry_decorator(max_retries=3)
    def _generate_sql_with_retry(self, question: str, attempt: int = 1) -> QueryResult:
        """Generate SQL query from a natural language question with retry logic."""
        logger.info(f"Generating SQL (Attempt {attempt})")
        schema = self._database.get_schema()
        prompt = SQL_GENERATION_TEMPLATE.format(
            db_type=self._database.db_type,
            schema=schema,
            question=question
        )
        if attempt > 1:
            prompt = SQL_CORRECTION_TEMPLATE.format(error="Previous attempt failed", question=question)

        temperature = self._initial_temperature + (attempt - 1) * self._temperature_increase
        logger.debug(f"Using temperature: {temperature}")

        logger.debug("SQL Generation Prompt:\n%s", prompt)
        sql = self._model.generate(prompt, max_tokens=self._max_tokens, stop=[";"], temperature=temperature)
        logger.info(f"Generated SQL: {sql}")
        return QueryResult(success=True, data=[sql])

    def _clean_sql_query(self, sql: str) -> str:
        """Clean and format the generated SQL query."""
        sql = re.sub(r'\s*(.+?)\s*(?=\1|\Z)', r'\1', sql)
        sql = re.sub(r'```\w*\n?|\n?```', '', sql)
        sql = sql.replace('`', '')
        return sql.strip()

    @retry_decorator(max_retries=3)
    def _execute_query_with_retry(self, sql: str, attempt: int = 1) -> QueryResult:
        """Execute the SQL query with retry logic."""
        logger.info(f"Executing query (Attempt {attempt}): {sql}")
        try:
            result = self._database.execute_query(sql)
            if result.success:
                logger.info(f"Query executed successfully on attempt {attempt}")
            return result
        except Exception as e:
            logger.error(f"Unexpected error during query execution: {str(e)}")
            return QueryResult(success=False, data=[], error_message=str(e))