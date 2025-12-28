from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from app.routers.db_router import router as db_router
from app.routers.file_upload import router as file_router
from app.routers.db_connection_router import router as db_connection_router
from app.auth import router as auth_router
from app.models import init_db, User, SessionLocal
from app.auth import hash_password

app = FastAPI(title="Multi-Database API", description="FastAPI with JWT Auth, Multi-DB Support, and File Upload")

# Initialize database
init_db()

# Create default admin user if it doesn't exist
def create_default_admin():
    db = SessionLocal()
    try:
        admin_user = db.query(User).filter(User.username == "admin").first()
        if not admin_user:
            admin_user = User(
                username="admin",
                hashed_password=hash_password("admin123")
            )
            db.add(admin_user)
            db.commit()
            print("✅ Default admin user created (username: admin, password: admin123)")
    except Exception as e:
        print(f"⚠️ Error creating default admin: {e}")
    finally:
        db.close()

create_default_admin()

# Include routers
app.include_router(auth_router)
app.include_router(db_router)
app.include_router(db_connection_router)
app.include_router(file_router)

# Serve static files (frontend)
static_dir = Path(__file__).parent.parent / "static"
static_dir.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


@app.get("/")
async def read_root():
    """Serve the frontend HTML page."""
    index_file = static_dir / "index.html"
    if index_file.exists():
        return FileResponse(str(index_file))
    return {"message": "Frontend not found. Please ensure static/index.html exists."}
