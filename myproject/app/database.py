from sqlalchemy import create_engine
from app.core.config import DATABASES

def get_connection(db_type: str):
    if db_type not in DATABASES:
        raise ValueError("Invalid database type. Choose oracle, postgres, mysql.")
    engine = create_engine(DATABASES[db_type])
    conn = engine.connect()
    return conn