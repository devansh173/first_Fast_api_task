from fastapi import APIRouter, HTTPException
from app.auth import authenticate_user, create_access_token

router = APIRouter(tags=["Auth"])


@router.post("/login")
def login(username: str, password: str):
    if not authenticate_user(username, password):
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    token = create_access_token({"sub": username})
    return {"access_token": token, "token_type": "bearer"}