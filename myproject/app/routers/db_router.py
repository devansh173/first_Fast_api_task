from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from app.schemas.db_schema import DBRequest
from app.database import get_connection
from app.auth import get_current_user

router = APIRouter(prefix="/db", tags=["Database"])


@router.post("/query")
async def run_query(
    data: DBRequest,
    current_user: str = Depends(get_current_user)  # Protected endpoint - requires authentication
):
    """
    Execute a SQL query on the specified database.
    
    Requires JWT authentication. Supports Oracle, PostgreSQL, and MySQL.
    Can use default connection strings from config or provide custom connection parameters.
    """
    conn = None
    try:
        # Get database connection
        conn = get_connection(
            db_type=data.db_type,
            host=data.host,
            port=data.port,
            database=data.database,
            username=data.username,
            password=data.password
        )
        
        # Execute query using text() for SQLAlchemy 2.0 compatibility
        # Use begin() to handle transactions properly
        with conn.begin():
            result = conn.execute(text(data.query))
            
            # Fetch results
            if result.returns_rows:
                rows = [dict(row._mapping) for row in result]
                return {
                    "status": "success",
                    "db_type": data.db_type,
                    "rows_affected": len(rows),
                    "data": rows
                }
            else:
                # For INSERT, UPDATE, DELETE queries
                # Transaction is automatically committed by the context manager
                return {
                    "status": "success",
                    "db_type": data.db_type,
                    "message": "Query executed successfully"
                }
            
    except ConnectionError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database connection error: {str(e)}"
        )
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"SQL error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}"
        )
    finally:
        if conn:
            conn.close()
