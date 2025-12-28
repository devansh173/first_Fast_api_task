from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from app.core.config import DATABASES
from typing import Optional


def build_connection_string(
    db_type: str,
    host: Optional[str] = None,
    port: Optional[int] = None,
    database: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None
) -> str:
    """Build a database connection string dynamically or use defaults."""
    # If all connection parameters are provided, build custom connection string
    if all([host, port, database, username, password]):
        if db_type == "oracle":
            return f"oracle+cx_oracle://{username}:{password}@{host}:{port}/{database}"
        elif db_type == "postgres":
            return f"postgresql://{username}:{password}@{host}:{port}/{database}"
        elif db_type == "mysql":
            return f"mysql+mysqlconnector://{username}:{password}@{host}:{port}/{database}"
    
    # Otherwise, use default from config
    if db_type not in DATABASES:
        raise ValueError("Invalid database type. Choose oracle, postgres, or mysql.")
    return DATABASES[db_type]


def get_connection(
    db_type: str,
    host: Optional[str] = None,
    port: Optional[int] = None,
    database: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None
):
    """Get a database connection using provided parameters or defaults."""
    connection_string = build_connection_string(
        db_type=db_type,
        host=host,
        port=port,
        database=database,
        username=username,
        password=password
    )
    
    try:
        engine = create_engine(connection_string, pool_pre_ping=True)
        conn = engine.connect()
        return conn
    except SQLAlchemyError as e:
        raise ConnectionError(f"Failed to connect to {db_type} database: {str(e)}")