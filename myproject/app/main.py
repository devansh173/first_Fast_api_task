from fastapi import FastAPI
from app.routers.db_router import router as db_router
from app.routers.file_upload import router as file_router
from app.auth import router as auth_router

app = FastAPI(title="Assignment Project")

app.include_router(auth_router)
app.include_router(db_router)
app.include_router(file_router)
