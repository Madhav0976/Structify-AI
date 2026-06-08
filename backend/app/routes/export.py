"""
Structify AI - Export Routes

Takes a StructuredDocument and a format_type,
returns the actual downloadable file or text string.
"""
import logging
from io import BytesIO
from fastapi import APIRouter, HTTPException, Response
from fastapi.responses import StreamingResponse

from app.schemas.structure import StructuredDocument
from app.services.formatters.engine import FormatEngine

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1", tags=["Export"])

# Instantiate the format engine
format_engine = FormatEngine()

@router.post(
    "/export",
    summary="Export AST to Markdown, DOCX, or PDF",
    description="Takes a parsed StructuredDocument and returns a downloadable file.",
)
async def export_document(
    document: StructuredDocument,
    format_type: str = "markdown"
):
    try:
        if not document.blocks:
            raise HTTPException(status_code=400, detail="Cannot export empty document.")

        logger.info(f"Exporting document as {format_type.upper()}...")
        
        # 1. Format the document (returns str or bytes)
        result = format_engine.format_document(document, format_type)
        
        # 2. Return the correct HTTP Response based on format type
        if format_type.lower() == "markdown":
            return Response(
                content=result,
                media_type="text/markdown",
                headers={"Content-Disposition": f'attachment; filename="structify_{document.document_type}.md"'}
            )
            
        elif format_type.lower() == "docx":
            # StreamingResponse for binary file
            buffer = BytesIO(result)
            return StreamingResponse(
                buffer,
                media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                headers={"Content-Disposition": f'attachment; filename="structify_{document.document_type}.docx"'}
            )
            
        elif format_type.lower() == "pdf":
            buffer = BytesIO(result)
            return StreamingResponse(
                buffer,
                media_type="application/pdf",
                headers={"Content-Disposition": f'attachment; filename="structify_{document.document_type}.pdf"'}
            )
            
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported format: {format_type}")

    except Exception as e:
        logger.error(f"Export failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Export failed: {str(e)}",
        )
