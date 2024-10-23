import logging
import re
from typing import Any, Tuple, Optional

from app.utils.query_result import QueryResult
from app.agents.prompt_templates import (
    SQL_GENERATION_TEMPLATE,
    SQL_CORRECTION_TEMPLATE,
    SQL_GENERATION_TEMPLATE_HRIDA
)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


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
        for attempt in range(1, self._max_retries + 1):
            temperature = self._initial_temperature + (attempt - 1) * self._temperature_increase

            if attempt == 1:
                sql_result = self._generate_sql(question, temperature)
            else:
                sql_result = self._generate_sql(question, temperature, previous_error)

            if not sql_result.success:
                return "", None, "Failed to generate SQL query"

            sql = sql_result.data[0]
            logger.info(f"Attempt {attempt} - Raw SQL: {sql}")
            cleaned_sql = self._clean_sql_query(sql)
            logger.info(f"Attempt {attempt} - Cleaned SQL: {cleaned_sql}")

            result = self._execute_query(cleaned_sql)
            if result.success:
                return cleaned_sql, result.data, None

            previous_error = result.error_message
            logger.warning(f"Attempt {attempt} failed. Error: {previous_error}")

            if attempt == self._max_retries:
                logger.error(f"All {self._max_retries} attempts failed.")
                return cleaned_sql, None, previous_error

    def _generate_sql(self, question: str, temperature: float, previous_error: str = None) -> QueryResult:
        """
        Generate SQL query from a natural language question.
        """
        schema = self._database.get_schema()
        model_name = self._model.metadata.get('general.name')
        if previous_error is None:
            # TODO: Dirty solution.
            #       Models should be matched with specific templates, if not the general will be used.
            if "hrida" in model_name.lower():
                prompt = SQL_GENERATION_TEMPLATE_HRIDA.format(
                    db_type=self._database.db_type,
                    schema=schema,
                    question=question
                )
            else:
                prompt = SQL_GENERATION_TEMPLATE.format(
                    db_type=self._database.db_type,
                    schema=schema,
                    question=question
                )
        else:
            if "hrida" in model_name.lower():
                logger(f"Model {model_name} is not supported for SQL correction")
            else:
                prompt = SQL_CORRECTION_TEMPLATE.format(
                    error=previous_error,
                    db_type=self._database.db_type,
                    question=question
                )
        logger.info("SQL Generation Prompt:\n%s", prompt)
        response = self._model(
            prompt,
            max_tokens=self._max_tokens,
            temperature=temperature,
            stop=[";"],
            echo=False
        )
        sql = response['choices'][0]['text'].strip()
        logger.info(f"Generated SQL: {sql}")
        return QueryResult(success=True, data=[sql])

    def _clean_sql_query(self, sql: str) -> str:
        """
        Clean and format the generated SQL query.
        """
        # Remove any leading special characters, whitespace, or unwanted tags
        sql = re.sub(r'^[\s\W]*', '', sql)

        # Remove any trailing special characters or whitespace
        sql = re.sub(r'[\s\W]*$', '', sql)

        # Remove any backticks
        sql = sql.replace('`', '')

        # Ensure the query starts with a SQL keyword
        sql_keywords = ['SELECT', 'INSERT', 'UPDATE', 'DELETE', 'CREATE', 'ALTER', 'DROP', 'TRUNCATE', 'WITH']
        if not any(sql.upper().startswith(keyword) for keyword in sql_keywords):
            # If it doesn't start with a SQL keyword, try to find the first occurrence
            for keyword in sql_keywords:
                keyword_index = sql.upper().find(keyword)
                if keyword_index != -1:
                    sql = sql[keyword_index:]
                    break

        return sql.strip()

    def _execute_query(self, sql: str) -> QueryResult:
        """
        Execute the SQL query.
        """
        logger.info(f"Executing query: {sql}")
        try:
            result = self._database.execute_query(sql)
            if result.success:
                logger.info("Query executed successfully")
            return result
        except Exception as e:
            error_message = str(e)
            logger.error(f"Unexpected error during query execution: {error_message}")
            return QueryResult(success=False, data=[], error_message=error_message)