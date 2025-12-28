from pydantic import BaseModel, Field
from typing import Optional


class DBRequest(BaseModel):
    """Schema for database query request with validation."""
    query: str = Field(..., min_length=1, description="SQL query to execute")
    
    # Option 1: Use stored connection by ID
    connection_id: Optional[int] = Field(None, description="ID of stored database connection")
    
    # Option 2: Provide connection details directly (if connection_id not provided)
    db_type: Optional[str] = Field(
        None,
        pattern="^(oracle|postgres|mysql)$",
        description="Database type: oracle, postgres, or mysql (required if connection_id not provided)"
    )
    host: Optional[str] = Field(None, description="Database host")
    port: Optional[int] = Field(None, description="Database port")
    database: Optional[str] = Field(None, description="Database name")
    username: Optional[str] = Field(None, description="Database username")
    password: Optional[str] = Field(None, description="Database password")
    
    class Config:
        json_schema_extra = {
            "example": {
                "db_type": "postgres",
                "query": "SELECT * FROM users LIMIT 10",
                "host": "localhost",
                "port": 5432,
                "database": "mydb",
                "username": "user",
                "password": "pass"
            }
        }
