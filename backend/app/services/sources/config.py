from enum import Enum


class SourceType(str, Enum):
    POSTGRESQL = "postgresql"
    MYSQL = "mysql"
    MONGODB = "mongodb"
    DATABRICKS = "databricks"
    CSV = "csv"
