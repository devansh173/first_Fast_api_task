from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List
from myproject.app.models import DatabaseConnection, get_db
from myproject.app.schemas.user_schema import (
    DatabaseConnectionCreate,
    DatabaseConnectionResponse,
    DatabaseConnectionUpdate
)
from myproject.app.auth import get_current_user

router = APIRouter(prefix="/db-connections", tags=["Database Connections"])


@router.post("", response_model=DatabaseConnectionResponse, status_code=status.HTTP_201_CREATED)
async def create_db_connection(
    connection_data: DatabaseConnectionCreate,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new database connection configuration."""
    # Check if connection name already exists for this user
    existing = db.query(DatabaseConnection).filter(
        DatabaseConnection.name == connection_data.name,
        DatabaseConnection.created_by == current_user
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Connection name already exists"
        )
    
    # Create new connection
    new_connection = DatabaseConnection(
        name=connection_data.name,
        db_type=connection_data.db_type,
        host=connection_data.host,
        port=connection_data.port,
        database=connection_data.database,
        username=connection_data.username,
        password=connection_data.password,
        created_by=current_user
    )
    
    db.add(new_connection)
    db.commit()
    db.refresh(new_connection)
    
    return new_connection


@router.get("", response_model=List[DatabaseConnectionResponse])
async def list_db_connections(
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all database connections for the current user."""
    connections = db.query(DatabaseConnection).filter(
        DatabaseConnection.created_by == current_user
    ).all()
    return connections


@router.get("/{connection_id}", response_model=DatabaseConnectionResponse)
async def get_db_connection(
    connection_id: int,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific database connection by ID."""
    connection = db.query(DatabaseConnection).filter(
        DatabaseConnection.id == connection_id,
        DatabaseConnection.created_by == current_user
    ).first()
    
    if not connection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Database connection not found"
        )
    
    return connection


@router.put("/{connection_id}", response_model=DatabaseConnectionResponse)
async def update_db_connection(
    connection_id: int,
    connection_data: DatabaseConnectionUpdate,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a database connection configuration."""
    connection = db.query(DatabaseConnection).filter(
        DatabaseConnection.id == connection_id,
        DatabaseConnection.created_by == current_user
    ).first()
    
    if not connection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Database connection not found"
        )
    
    # Update fields if provided
    update_data = connection_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(connection, field, value)
    
    db.commit()
    db.refresh(connection)
    
    return connection


@router.delete("/{connection_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_db_connection(
    connection_id: int,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a database connection configuration."""
    connection = db.query(DatabaseConnection).filter(
        DatabaseConnection.id == connection_id,
        DatabaseConnection.created_by == current_user
    ).first()
    
    if not connection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Database connection not found"
        )
    
    db.delete(connection)
    db.commit()
    
    return None

