"""
Structify AI - OCR Service

This is the core OCR engine that wraps EasyOCR.

WHY A SERVICE LAYER?
  - Routes should only handle HTTP logic (receive request → send response)
  - Services contain the actual business logic (process the image)
  - This separation means we can:
      - Swap EasyOCR for another engine later without touching routes
      - Unit test the OCR logic independently
      - Reuse OCR logic from multiple routes

HOW EASYOCR WORKS:
  1. We create a Reader with language(s) we want to support
  2. We feed it an image (file path or numpy array)
  3. It returns a list of detections: [bbox, text, confidence]
  4. bbox = [[x1,y1], [x2,y2], [x3,y3], [x4,y4]] (4 corners of the text box)
"""

import logging
from pathlib import Path

import easyocr

from app.schemas.ocr import OCRTextBlock, OCRResponse

# Set up logging for this module
logger = logging.getLogger(__name__)

# ============================================================
# EasyOCR Reader — Singleton Pattern
# ============================================================
# We create the reader ONCE and reuse it for all requests.
# Creating it is slow (~2-5 seconds) because it loads the AI model.
# But once loaded, each OCR call is fast.

_reader: easyocr.Reader | None = None


def get_reader() -> easyocr.Reader:
    """
    Get or create the EasyOCR reader (singleton).

    First call: loads the model (~2-5 seconds)
    Subsequent calls: returns the already-loaded reader instantly
    """
    global _reader
    if _reader is None:
        logger.info("Loading EasyOCR model (first time — this takes a few seconds)...")
        _reader = easyocr.Reader(
            ["en"],          # Languages to support (English for now)
            gpu=False,       # Use CPU (set True if you have a compatible GPU)
        )
        logger.info("EasyOCR model loaded successfully!")
    return _reader


def extract_text_from_image(image_path: str) -> OCRResponse:
    """
    Extract text from an image file using EasyOCR.

    Args:
        image_path: Absolute path to the image file

    Returns:
        OCRResponse with extracted text, blocks, and confidence scores

    How it works:
        1. Validate the file exists
        2. Run EasyOCR on the image
        3. Parse each detection into an OCRTextBlock
        4. Combine all text into raw_text
        5. Calculate average confidence
        6. Return structured response
    """
    # --- Step 1: Validate file exists ---
    file_path = Path(image_path)
    if not file_path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    filename = file_path.name
    logger.info(f"Starting OCR extraction for: {filename}")

    # --- Step 2: Run EasyOCR ---
    reader = get_reader()
    # detail=1 returns: list of [bbox, text, confidence]
    results = reader.readtext(str(file_path), detail=1)

    # --- Step 3: Parse results into structured blocks ---
    blocks: list[OCRTextBlock] = []
    for bbox, text, confidence in results:
        # EasyOCR returns bbox as list of lists with float coords
        # Convert to integer pixel coordinates
        bbox_int = [[int(coord) for coord in point] for point in bbox]

        blocks.append(
            OCRTextBlock(
                text=text.strip(),
                confidence=round(float(confidence), 4),
                bbox=bbox_int,
            )
        )

    # --- Step 4: Combine all text ---
    # Join blocks with newline to preserve some structure
    raw_text = "\n".join(block.text for block in blocks)

    # --- Step 5: Calculate average confidence ---
    if blocks:
        avg_confidence = round(
            sum(b.confidence for b in blocks) / len(blocks), 4
        )
    else:
        avg_confidence = 0.0

    logger.info(
        f"OCR complete for {filename}: "
        f"{len(blocks)} blocks, avg confidence {avg_confidence}"
    )

    # --- Step 6: Return structured response ---
    return OCRResponse(
        success=True,
        filename=filename,
        raw_text=raw_text,
        blocks=blocks,
        total_blocks=len(blocks),
        average_confidence=avg_confidence,
    )
