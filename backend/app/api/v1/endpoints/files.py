from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import os
import shutil

router = APIRouter()


@router.post("/validate")
async def validate_file(filepath: dict):
    """Validate file path from frontend"""
    input_path = filepath.get("filepath", "")

    # Normalize and validate file path
    if not os.path.exists(input_path):
        raise HTTPException(status_code=400, detail="File does not exist")

    # Ensure file is within allowed directories
    allowed_dirs = ["/app/data", "/tmp/uploads"]
    normalized_path = os.path.normpath(input_path)

    if not any(
        normalized_path.startswith(os.path.normpath(allowed_dir))
        for allowed_dir in allowed_dirs
    ):
        raise HTTPException(status_code=403, detail="File access not permitted")

    return {"valid": True, "normalized_path": normalized_path}


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Handle file upload to backend"""
    # Validate file type
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")

    try:
        upload_dir = "/app/data"
        os.makedirs(upload_dir, exist_ok=True)

        # Create a safe filename
        safe_filename = os.path.basename(file.filename)
        filepath = os.path.join(upload_dir, safe_filename)

        # Save uploaded file
        with open(filepath, "wb") as buffer:
            content = await file.read()
            buffer.write(content)

        return {"filepath": filepath, "filename": safe_filename}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while uploading the file: {str(e)}",
        )
