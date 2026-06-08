"""
Structify AI - OCR Routes

Handles image upload and OCR extraction endpoints.

HOW FILE UPLOAD WORKS IN FASTAPI:
  1. The user sends a POST request with an image file
  2. FastAPI receives it as an UploadFile object
  3. We save it temporarily to disk (uploads/ folder)
  4. We pass the file path to our OCR service
  5. We return the extracted text
  6. We clean up the temporary file
"""

import os
import logging
from pathlib import Path

from fastapi import APIRouter, UploadFile, File, HTTPException

from app.services.ocr_service import extract_text_from_image
from app.schemas.ocr import OCRResponse, OCRErrorResponse

# Set up logging
logger = logging.getLogger(__name__)

# Create the router
router = APIRouter(prefix="/api/v1", tags=["OCR"])

# Directory where uploaded files are temporarily stored
UPLOAD_DIR = Path(__file__).resolve().parent.parent.parent / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

# Allowed image file extensions
ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".webp"}

# Maximum file size: 10 MB
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB in bytes


@router.post(
    "/ocr/extract",
    response_model=OCRResponse,
    responses={
        400: {"model": OCRErrorResponse, "description": "Invalid file"},
        500: {"model": OCRErrorResponse, "description": "OCR processing failed"},
    },
    summary="Extract text from an image",
    description=(
        "Upload an image file and extract text using EasyOCR. "
        "Returns the raw text, individual text blocks with confidence "
        "scores, and bounding box coordinates."
    ),
)
async def extract_text(
    file: UploadFile = File(
        ...,
        description="Image file to extract text from (PNG, JPG, BMP, TIFF, WebP)",
    ),
):
    """
    Extract text from an uploaded image.

    Steps:
        1. Validate file type and size
        2. Save file temporarily
        3. Run OCR extraction
        4. Return structured result
        5. Clean up temp file
    """
    saved_path: Path | None = None

    try:
        # --- Step 1: Validate file type ---
        if not file.filename:
            raise HTTPException(
                status_code=400,
                detail="No filename provided.",
            )

        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=(
                    f"File type '{file_ext}' is not supported. "
                    f"Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
                ),
            )

        # --- Step 2: Read and validate file size ---
        contents = await file.read()

        if len(contents) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=(
                    f"File too large ({len(contents) / 1024 / 1024:.1f} MB). "
                    f"Maximum size is {MAX_FILE_SIZE / 1024 / 1024:.0f} MB."
                ),
            )

        if len(contents) == 0:
            raise HTTPException(
                status_code=400,
                detail="Uploaded file is empty.",
            )

        # --- Step 3: Save file temporarily ---
        saved_path = UPLOAD_DIR / file.filename
        with open(saved_path, "wb") as f:
            f.write(contents)

        logger.info(f"File saved: {saved_path} ({len(contents)} bytes)")

        # --- Step 4: Run OCR extraction ---
        result = extract_text_from_image(str(saved_path))

        return result

    except HTTPException:
        # Re-raise HTTP exceptions as-is (validation errors)
        raise

    except Exception as e:
        logger.error(f"OCR extraction failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"OCR extraction failed: {str(e)}",
        )

    finally:
        # --- Step 5: Clean up temp file ---
        if saved_path and saved_path.exists():
            os.remove(saved_path)
            logger.info(f"Temp file cleaned up: {saved_path}")
