from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    """Schema for user registration."""
    username: str = Field(..., min_length=3, max_length=50, description="Username (3-50 characters)")
    password: str = Field(..., min_length=6, description="Password (minimum 6 characters)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "username": "john_doe",
                "password": "securepassword123"
            }
        }


class UserResponse(BaseModel):
    """Schema for user response."""
    id: int
    username: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class DatabaseConnectionCreate(BaseModel):
    """Schema for creating a database connection."""
    name: str = Field(..., min_length=1, max_length=100, description="Connection name")
    db_type: str = Field(..., pattern="^(oracle|postgres|mysql)$", description="Database type")
    host: str = Field(..., description="Database host")
    port: int = Field(..., gt=0, le=65535, description="Database port")
    database: str = Field(..., description="Database name")
    username: str = Field(..., description="Database username")
    password: str = Field(..., description="Database password")
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Production PostgreSQL",
                "db_type": "postgres",
                "host": "localhost",
                "port": 5432,
                "database": "mydb",
                "username": "dbuser",
                "password": "dbpass"
            }
        }


class DatabaseConnectionResponse(BaseModel):
    """Schema for database connection response."""
    id: int
    name: str
    db_type: str
    host: str
    port: int
    database: str
    username: str
    created_by: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class DatabaseConnectionUpdate(BaseModel):
    """Schema for updating a database connection."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    host: Optional[str] = None
    port: Optional[int] = Field(None, gt=0, le=65535)
    database: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None

