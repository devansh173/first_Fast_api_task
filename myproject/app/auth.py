from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from jose import jwt, JWTError
import bcrypt
from app.core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(prefix="/auth", tags=["Authentication"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Demo user - In production, this should be stored in a database
# Default credentials: username="admin", password="admin123"
FAKE_USER = {
    "username": "admin",
    "hashed_password": "$2b$12$9z5Sc3IIG2jSUeIIt/TYVewqdLGc3V8P24rlr4YZwbNwhYTF7yRLW"  # password: "admin123"
}


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    password_bytes = password.encode("utf-8")
    if len(password_bytes) > 72:
        raise ValueError("Password too long. Maximum is 72 bytes for bcrypt.")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash."""
    try:
        password_bytes = plain_password.encode("utf-8")
        hashed_bytes = hashed_password.encode("utf-8")
        return bcrypt.checkpw(password_bytes, hashed_bytes)
    except Exception:
        return False


def authenticate_user(username: str, password: str) -> bool:
    """Authenticate a user by username and password."""
    if username != FAKE_USER["username"]:
        return False
    return verify_password(password, FAKE_USER["hashed_password"])


def create_access_token(data: dict):
    """Create a JWT access token."""
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data.update({"exp": expire})
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Dependency to get the current authenticated user from JWT token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username
    except JWTError:
        raise credentials_exception


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login endpoint to authenticate and get JWT token."""
    if not authenticate_user(form_data.username, form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/verify")
async def verify_token(current_user: str = Depends(get_current_user)):
    """Verify if the current JWT token is valid."""
    return {"message": "Token is valid", "username": current_user}


@router.get("/me")
async def read_users_me(current_user: str = Depends(get_current_user)):
    """Get current authenticated user information."""
    return {"username": current_user}
