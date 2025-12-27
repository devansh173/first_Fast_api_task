from pydantic import BaseModel, Field

class DBRequest(BaseModel):
    db_type: str = Field(..., pattern="^(oracle|postgres|mysql)$")
    query: str
