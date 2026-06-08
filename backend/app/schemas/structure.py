"""
Structify AI - Structure Schemas

Defines the structure tree built from raw OCR blocks.
"""

from enum import Enum
from pydantic import BaseModel, Field

class BlockType(str, Enum):
    TITLE = "title"           # Document main title
    HEADING = "heading"       # Section header (H1)
    SUBHEADING = "subheading" # Sub-section header (H2, H3)
    PARAGRAPH = "paragraph"   # Standard body text
    LIST_ITEM = "list_item"   # Bullet points, numbered lists
    UNKNOWN = "unknown"       # Fallback

class StructuredBlock(BaseModel):
    """A semantic block of text mapped from an OCR block."""
    id: int
    type: BlockType
    text: str
    level: int = 0  # 1 for H1, 2 for H2 (only relevant for headings/lists)
    metadata: dict = Field(
        default_factory=dict,
        description="Stores confidence, original bbox, font_size_proxy, etc.",
    )

class StructuredDocument(BaseModel):
    """The final processed document AST (Abstract Syntax Tree)."""
    document_type: str = Field(..., description="E.g., generic, resume, report")
    blocks: list[StructuredBlock]
    total_blocks: int

# Need to import OCRResponse for the request schema
from app.schemas.ocr import OCRResponse

class StructureAnalyzeRequest(BaseModel):
    """
    The request payload for the structure analysis endpoint.
    Wraps the raw OCR data and allows per-request feature flags.
    """
    ocr_data: OCRResponse
    enable_repair: bool | None = Field(
        default=None, 
        description="Override the global config to enable/disable OCR Error Repair."
    )
    doc_type: str = Field(
        default="auto",
        description="Force a specific document type detector (e.g., 'report', 'resume'), or 'auto' to classify."
    )
