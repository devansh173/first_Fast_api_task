from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, status
import shutil
import os
from pathlib import Path
from myproject.app.auth import get_current_user

router = APIRouter(prefix="/upload", tags=["File Upload"])

# Configuration
UPLOAD_DIR = Path("uploads")
MAX_FILE_SIZE = 10 * 1024 * 1024 * 1024  # 10GB default limit
CHUNK_SIZE = 1024 * 1024  # 1MB chunks for efficient streaming


@router.post("/bigfile")
async def upload_big_file(
    file: UploadFile = File(...),
    current_user: str = Depends(get_current_user)  # Protected endpoint - requires authentication
):
    """
    Upload large files efficiently using streaming.
    
    Features:
    - Handles large files efficiently using chunked streaming
    - Creates uploads directory if it doesn't exist
    - Validates file size
    - Requires JWT authentication
    """
    # Create uploads directory if it doesn't exist
    UPLOAD_DIR.mkdir(exist_ok=True)
    
    # Validate file size (if Content-Length is provided)
    if hasattr(file, 'size') and file.size:
        if file.size > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File too large. Maximum size is {MAX_FILE_SIZE / (1024**3):.2f} GB"
            )
    
    # Generate safe file path
    safe_filename = file.filename.replace(" ", "_").replace("/", "_").replace("\\", "_")
    file_location = UPLOAD_DIR / safe_filename
    
    try:
        # Stream file in chunks for memory efficiency
        with open(file_location, "wb") as buffer:
            total_size = 0
            while True:
                chunk = await file.read(CHUNK_SIZE)
                if not chunk:
                    break
                total_size += len(chunk)
                
                # Check size during upload (if Content-Length wasn't available)
                if total_size > MAX_FILE_SIZE:
                    # Clean up partial file
                    if file_location.exists():
                        file_location.unlink()
                    raise HTTPException(
                        status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                        detail=f"File too large. Maximum size is {MAX_FILE_SIZE / (1024**3):.2f} GB"
                    )
                
                buffer.write(chunk)
        
        file_size_mb = total_size / (1024 * 1024)
        
        return {
            "message": "File uploaded successfully",
            "filename": safe_filename,
            "file_path": str(file_location),
            "size_mb": round(file_size_mb, 2),
            "uploaded_by": current_user
        }
        
    except HTTPException:
        raise
    except Exception as e:
        # Clean up partial file on error
        if file_location.exists():
            file_location.unlink()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error uploading file: {str(e)}"
        )
