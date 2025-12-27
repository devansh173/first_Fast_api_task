from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from jose import jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from app.core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

fake_user = {"username": "admin", "password": pwd_context.hash("admin123"[:72])}

def create_access_token(data: dict):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data.update({"exp": expire})
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def authenticate_user(username: str, password: str):
    if username == fake_user["username"] and pwd_context.verify(password, fake_user["password"]):
        return True
    return False

def require_token(token: str = Depends(oauth2_scheme)):
    try:
        jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return True
    except:
        raise HTTPException(status_code=401, detail="Invalid token")
