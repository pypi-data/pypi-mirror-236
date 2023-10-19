import enum


class SQLDialect(enum.Enum):
    BIGQUERY = "BIGQUERY"
    SNOWFLAKE = "SNOWFLAKE"
    REDSHIFT = "REDSHIFT"


class FORMAT(enum.Enum):
    PLAIN = "PLAIN"
    ENV = "ENV"
