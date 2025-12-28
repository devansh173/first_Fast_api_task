from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.schemas.db_schema import DBRequest
from app.database import get_connection
from app.auth import get_current_user
from app.models import DatabaseConnection, get_db

router = APIRouter(prefix="/db", tags=["Database"])


@router.post("/query")
async def run_query(
    data: DBRequest,
    current_user: str = Depends(get_current_user),  # Protected endpoint - requires authentication
    db: Session = Depends(get_db)
):
    """
    Execute a SQL query on the specified database.
    
    Requires JWT authentication. Supports Oracle, PostgreSQL, and MySQL.
    Can use stored connection by ID or provide connection parameters directly.
    """
    conn = None
    try:
        # If connection_id is provided, use stored connection
        if data.connection_id:
            stored_conn = db.query(DatabaseConnection).filter(
                DatabaseConnection.id == data.connection_id,
                DatabaseConnection.created_by == current_user
            ).first()
            
            if not stored_conn:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Database connection not found"
                )
            
            conn = get_connection(
                db_type=stored_conn.db_type,
                host=stored_conn.host,
                port=stored_conn.port,
                database=stored_conn.database,
                username=stored_conn.username,
                password=stored_conn.password
            )
            db_type = stored_conn.db_type
        else:
            # Use provided connection parameters
            if not data.db_type:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Either connection_id or db_type must be provided"
                )
            
            conn = get_connection(
                db_type=data.db_type,
                host=data.host,
                port=data.port,
                database=data.database,
                username=data.username,
                password=data.password
            )
            db_type = data.db_type
        
        # Execute query using text() for SQLAlchemy 2.0 compatibility
        # Use begin() to handle transactions properly
        with conn.begin():
            result = conn.execute(text(data.query))
            
            # Fetch results
            if result.returns_rows:
                rows = [dict(row._mapping) for row in result]
                return {
                    "status": "success",
                    "db_type": db_type,
                    "rows_affected": len(rows),
                    "data": rows
                }
            else:
                # For INSERT, UPDATE, DELETE queries
                # Transaction is automatically committed by the context manager
                return {
                    "status": "success",
                    "db_type": db_type,
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
