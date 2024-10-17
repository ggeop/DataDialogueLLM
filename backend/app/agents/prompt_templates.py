
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
"""