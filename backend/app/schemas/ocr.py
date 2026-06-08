"""
Structify AI - OCR Schemas

Defines the data shapes for OCR requests and responses.

WHY SCHEMAS?
  - They validate incoming data automatically
  - They document what the API expects/returns
  - They show up in the Swagger docs (/docs)
  - They prevent bugs by catching bad data early
"""

from pydantic import BaseModel, Field


class OCRTextBlock(BaseModel):
    """
    A single block of text detected by OCR.

    Each block has:
      - text: the actual text detected
      - confidence: how sure the OCR engine is (0.0 to 1.0)
      - bbox: bounding box coordinates [[x1,y1], [x2,y2], [x3,y3], [x4,y4]]
    """
    text: str = Field(..., description="The detected text content")
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="OCR confidence score (0.0 = uncertain, 1.0 = very confident)",
    )
    bbox: list[list[int]] = Field(
        ...,
        description="Bounding box coordinates: [[x1,y1], [x2,y2], [x3,y3], [x4,y4]]",
    )


class OCRResponse(BaseModel):
    """
    The complete response from an OCR extraction.

    Contains:
      - success: whether the OCR worked
      - filename: name of the uploaded file
      - raw_text: all detected text joined together
      - blocks: individual text blocks with position + confidence
      - total_blocks: count of detected text blocks
      - average_confidence: overall confidence score
    """
    success: bool = Field(..., description="Whether OCR extraction succeeded")
    filename: str = Field(..., description="Original filename of the uploaded image")
    raw_text: str = Field(
        ...,
        description="All detected text combined into a single string",
    )
    blocks: list[OCRTextBlock] = Field(
        default=[],
        description="Individual text blocks with position and confidence",
    )
    total_blocks: int = Field(
        ...,
        description="Total number of text blocks detected",
    )
    average_confidence: float = Field(
        ...,
        description="Average confidence across all detected blocks",
    )


class OCRErrorResponse(BaseModel):
    """Response returned when OCR extraction fails."""
    success: bool = Field(default=False)
    error: str = Field(..., description="Description of what went wrong")
    filename: str = Field(default="", description="Original filename if available")
