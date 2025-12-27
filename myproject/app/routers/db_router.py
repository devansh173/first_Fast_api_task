from fastapi import APIRouter, HTTPException
from app.schemas.db_schema import DBRequest
from app.database import get_connection

router = APIRouter(prefix="/db", tags=["Database"])

@router.post("/query")
def run_query(data: DBRequest):
    try:
        conn = get_connection(data.db_type)
        result = conn.execute(data.query)
        rows = [dict(row) for row in result]  # convert to JSON serializable
        conn.close()
        return {"status": "success", "data": rows}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
