from fastapi import APIRouter, UploadFile, File
import shutil

router = APIRouter(prefix="/upload", tags=["File Upload"])

@router.post("/bigfile")
async def upload_big_file(file: UploadFile = File(...)):
    file_location = f"uploads/{file.filename}"

    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)  # streams in chunks (efficient)

    return {"message": "File uploaded successfully", "file_path": file_location}
